from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Comment(models.Model):

    user = models.ForeignKey(User)
    parent = models.ForeignKey('Comment', null=True)

    title = models.TextField()
    level = models.IntegerField(default=0)
    text = models.TextField()
    deleted = models.DateTimeField(null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
