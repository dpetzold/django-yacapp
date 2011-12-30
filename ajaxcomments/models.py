from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):

    user_id = models.ForeignKey(User)

    title = models.TextField()
    text = models.TextField()
    deleted = models.DateTimeField(null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    modified = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)


