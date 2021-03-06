from django.utils.timesince import timesince
from django.utils.html import escape
from django.db import models as django_models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.template import loader, RequestContext, Context
from django.utils import html

import datetime
import json
import logging
import time

from dakku.ajax import AjaxResponse
from dakku import log

from yacapp import signals
from yacapp import models

import logging

logger = logging.getLogger(__name__)

class GetContentObjectError(Exception):
    pass

# Taken from django/contrib/comments/views/comments.py:post_comment
def get_content_object(content_type, object_pk):

    # Look up the object we're trying to comment about
    if content_type is None or object_pk is None:
        raise GetContentObjectError('Missing content_type or object_pk field.')
    try:
        model = django_models.get_model(*content_type.split('.', 1))
        content_object = model._default_manager.using(None).get(pk=object_pk)
    except TypeError:
        raise GetContentObjectError('Invalid content_type value: %r' % escape(content_type))
    except AttributeError:
        raise GetContentObjectError('The given content-type %r does not resolve to a valid model.' % \
                escape(content_type))
    except ObjectDoesNotExist:
        raise GetContentObjectError('No object matching content-type %r and object PK %r exists.' % \
                (escape(content_type), escape(object_pk)))
    except (ValueError, ValidationError), e:
        raise GetContentObjectError(
            'Attempting go get content-type %r and object PK %r exists raised %s' % \
                (escape(content_type), escape(object_pk), e.__class__.__name__))
    return content_object

def comment_post(request, template='comment.html'):

    if not request.user.is_authenticated():
        return AjaxResponse(False, error='User must be authenticated')

    if not request.POST:
        return AjaxResponse(False, error='Post required')

    comment_text = html.escape(request.POST['text'])
    if len(comment_text) == 0:
        return AjaxResponse(False, error='Comment must contain some text %s' %
                (len(comment_text)))

    content_object = get_content_object(
        request.POST.get('content_type'),
        request.POST.get('object_pk'))

    comment = models.Comment(
        user=request.user,
        content_object=content_object,
        text=comment_text)

    if 'title' in request.POST:
        comment.title = request.POST['title']
    if 'parent_id' in request.POST:
        comment.parent = models.Comment.objects.get(
                pk=int(request.POST['parent_id'].replace('comment-', '')))
        comment.level = comment.parent.level + 1

    comment.save()

    content_object.comment_count += 1
    content_object.save()

    logger.info('%s added a comment' % (request.user))

    signals.comment_was_posted.send(
        sender=comment.__class__,
        comment=comment,
        request=request,
    )

    return AjaxResponse(True,
            comment=loader.render_to_string(template, {
                'comment':comment,
            }, context_instance=RequestContext(request)),
            comment_count=content_object.comment_count)

@log.logger()
def comment_edit(request, template='include/comment.html', logger=None):

    if not request.user.is_authenticated():
        return AjaxResponse(False, error='User must be authenticated')

    if not request.POST:
        return AjaxResponse(False, error='Post required')

    try:
        comment = models.Comment.objects.get(
            id=request.POST['comment_id'].replace('comment-', ''))
    except models.Comment.DoesNotExist as e:
        return AjaxResponse(False, error=str(e))

    try:
        text = request.POST['text']
    except MultiValueDictKeyError as e:
        logger.error(str(e))
        return AjaxResponse(False, error=str(e))

    if request.user != comment.user:
        logger.info('Unauthorized comment edit by ' % (request.user))
        return AjaxResponse(False, error='Not authorizied')

    comment.text = text
    comment.save()

    logger.info('%s edited a comment' % (request.user))

    return AjaxResponse(True, text=comment.text)

@log.logger()
def comment_delete(request, logger=None):

    if not request.user.is_authenticated():
        return AjaxResponse(False, error='User must be authenticated')

    content_object = get_content_object(
        request.POST.get('content_type'),
        request.POST.get('object_pk'))

    try:
        comment = models.Comment.objects.get(
            id=request.POST['comment_id'].replace('comment-', ''))
    except models.Comment.DoesNotExist as e:
        return AjaxResponse(False, error=str(e))

    if request.user != comment.user:
        logger.info('Unauthorized comment deletion by ' % (request.user))
        return AjaxResponse(False, error='Not authorizied')

    comment.deleted = datetime.datetime.now()
    comment.save()

    content_object.comment_count -= 1
    content_object.save()

    logger.info('%s deleted a comment' % (request.user))
    return AjaxResponse(True,
            comment_count=content_object.comment_count)
