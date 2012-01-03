
from django.conf.urls.defaults import patterns, url

from ajaxcomments import views

urlpatterns = patterns('',
    url(r'^delete/(?P<comment_id>[\w\-]+)/', views.comment_delete, name='comment-delete'),
    url(r'^edit/(?P<comment_id>[\w\-]+)/', views.comment_edit, name='comment-edit'),
    url(r'^post/', views.comment_post, name='comment-post'),
)
