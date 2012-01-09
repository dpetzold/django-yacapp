from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

import logging

register = template.Library()

logger = logging.getLogger('django.ajaxcomments')

class RenderComments(template.Node):

    def __init__(self, object_expr=None):
        self.object_expr = object_expr

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_form and return a Node."""
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" %          tokens[0])

        # {% render_comment_form for obj %}
        if len(tokens) == 3:
            return cls(object_expr=parser.compile_filter(tokens[2]))

    def render_comment(self, obj, comment, context):

       replies = ''
       for child in obj.comments.filter(parent=comment).order_by('created'):
           replies += self.render_comment(obj, child, context)

       text = render_to_string(
               'comment.html', {
                   'comment': comment,
                   'replies': replies,
                },
               context)

       return text

    def render(self, context):

        obj = self.object_expr.resolve(context)

        comments = obj.comments.filter(
            parent__isnull=True,
            deleted__isnull=True)

        comments_text = ''
        for comment in comments:
            comments_text += self.render_comment(obj, comment, context)
        return comments_text

def render_comments(parser, token):
    return RenderComments.handle_token(parser, token)

register.tag('comments', render_comments)
