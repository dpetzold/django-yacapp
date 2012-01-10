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

from dago.ajax import AjaxResponse
from dago import log

#from ajaxcomments import signals
from ajaxcomments import models

import logging

logger = logging.getLogger('django.ajaxcomments')

def comment_post(request, template='comment.html'):

    if not request.user.is_authenticated():
        return AjaxResponse(False, error='User must be authenticated')

    if not request.POST:
        return AjaxResponse(False, error='Post required')

    comment_text = html.escape(request.POST['text'])
    if len(comment_text) == 0:
        return AjaxResponse(False, error='Comment must contain some text %s' %
                (len(comment_text)))

    # Look up the object we're trying to comment about
    content_type = request.POST.get('content_type')
    object_pk = request.POST.get('object_pk')
    if content_type is None or object_pk is None:
        return AjaxResponse(False, error='Missing content_type or object_pk field.')
    try:
        model = django_models.get_model(*content_type.split('.', 1))
        content_object = model._default_manager.using(None).get(pk=object_pk)
    except TypeError:
        return AjaxResponse(False,
            error='Invalid content_type value: %r' % escape(content_type))
    except AttributeError:
        return AjaxResponse(False,
            error='The given content-type %r does not resolve to a valid model.' % \
                escape(content_type))
    except ObjectDoesNotExist:
        return AjaxResponse(False,
            error='No object matching content-type %r and object PK %r exists.' % \
                (escape(content_type), escape(object_pk)))
    except (ValueError, ValidationError), e:
        return AjaxResponse(False,
            error='Attempting go get content-type %r and object PK %r exists raised %s' % \
                (escape(content_type), escape(object_pk), e.__class__.__name__))

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

    logger.info('%s added a comment %s' % (request.user, comment.user))
    return AjaxResponse(True,
            comment=loader.render_to_string(template, {
                'comment':comment,
            }, context_instance=RequestContext(request)),
            comment_count=content_object.comments.all().count())

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

    logger.info('%s deleted a comment' % (request.user))
    return AjaxResponse(True)
