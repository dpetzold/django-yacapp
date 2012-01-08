from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
register = template.Library()


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

        # {% render_comment_form for app.models pk %}
#        elif len(tokens) == 4:
#            return cls(
#                ctype = BaseCommentNode.lookup_content_type(tokens[2], tokens[0]),
#                object_pk_expr = parser.compile_filter(tokens[3])
#            )

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

    def render(self, context):

        content_type, object_pk = self.get_target_ctype_pk(context)

        obj = self.object_expr.resolve(context)

        comments = obj.comments.filter(
            parent__isnull=True,
            deleted__isnull=True)

        form_str = render_to_string("comment.html", {'comment': comments[0]}, context)
        context.pop()
        return form_str

def render_comments(parser, token):

    return RenderComments.handle_token(parser, token)

register.tag('comments', render_comments)
