from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

import logging

register = template.Library()

logger = logging.getLogger(__name__)

class RenderComments(template.Node):

    def __init__(self, object_expr, template):
        self.object_expr = object_expr
        self.template = template

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_form and return a Node."""
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" %          tokens[0])

        if tokens[3] != 'with':
            raise template.TemplateSyntaxError("Thrid argument in %r tag must be 'with'" %          tokens[0])

        # {% render_comment_form for obj %}
        if len(tokens) == 5:
            return cls(
                parser.compile_filter(tokens[2]),
                tokens[4].strip('"'))
        raise template.TemplateSyntaxError('Wrong number of arguments')

    def render_comment(self, obj, comment, context):

        replies = ''
        childern = obj.comments.filter(parent=comment)
        for child in childern.order_by('created'):
           replies += self.render_comment(obj, child, context)

        if replies == '':
            replies = None

        text = render_to_string(
               self.template, {
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

        comment_text = ''
        for comment in comments:
            comment_text += self.render_comment(obj, comment, context)
        return comment_text

def render_comments(parser, token):
    return RenderComments.handle_token(parser, token)

register.tag('comments', render_comments)
