Yet Another Commenting App
==========================
**Django commenting app that works something like hackernews.**

Supports message threading, ajax and email notifications. It is the commenting 
system used on my blog at https://derrickpetzold.com (demos are there). I wrote it
since I just wanted really simple commenting support and from what I could tell
there was not an app out there that did everything I wanted. Ie one would
support ajax but not threading etc. I also had a difficuly time finding demos
of the existing apps but I honestly didn't look very hard since I was looking
for excuse to create an app anyways.

The reason is doesn't use django.contrib.comments is probably not a good one.
I just didn't need all the stuff in there like moderation, anonymous posting
etc. The interesting work was in the template rendering so if you just want to 
take that go for it.

.. contents:: Contents
    :depth: 5

Installation
------------
#. Get the source.

    pip install -e git+https://github.com/dpetzold/django-yacapp

#. Add yacapp to INSTALLED_APPS your project's ``settings.py``

    'yacapp',

#. Add url include to your project's ``urls.py``

    (r'^comments/', include('yacapp.urls')),

#. Ensure ``django-yacapp`` static media is accessible, see `managing static files <https://docs.djangoproject.com/en/dev/howto/static-files/>`_.

#. Run syncdb

    python manage.py syncdb

Usage
-----

#. Update your models to support the generic relation.::

    comments = generic.GenericRelation(yacapp_models.Comment,
                content_type_field='content_type',
                object_id_field='object_id')

    comment_count = models.IntegerField(default=0)

#. Create your template for posting and displaying the comments. Requires
`jQuery <http://jquery.com/>` and `jQuery UI <http://jqueryui.com/>` for
the dialog popups.::

    {% yacapp_tags %}

    {% with comment_count=post.comment_count %}
    <h2 class="comment-count">{{ comment_count }} Comment{{ comment_count|pluralize }}</h2>
    <hr/>
    {% endwith %}

    <div class="comments">
      {% comments for post with "include/comment.html" %}
    </div>

    <div class="comment-edit" title="Edit comment">
      <form action="#">
        <input type="hidden" id="comment_id"></input>
        <div class="fieldWrapper lastFieldWrapper">
          <label for="id_edit">Edit:</label>
          <textarea id="id_edit"></textarea>
        </div>
        <button class="edit-save" type="submit">Save</button>
      </form>
    </div>

    <div class="comment-reply" title="Reply to comment">
      <p class="comment-text"></p>
      <form action="#">
        <input type="hidden" id="parent_id"></input>
        <div class="fieldWrapper lastFieldWrapper">
          <label for="id_reply">Reply:</label>
          <textarea id="id_reply"></textarea>
        </div>
        <button class="post-reply" type="submit">Save</button>
      </form>
    </div>

    <div class="comment-form">
      <form action="#">

          <label class="comment-label" for="id_text">
          Comment as <span class="display-name">{{ request.user.get_profile.display_name }}</span> (<a class="change- settings" href="#">change</a>):</label>

          <textarea id="id_text"></textarea>
        <button class="post-button" type="submit">Post</button>
      </form>
    </div>

#. Create your template for displaying the comment.::

    <div class="comment level-{{ comment.level }}" id="comment-{{ comment.id }}">
      <p id="p-{{ comment.id }}">{{ comment.text|safe }}</p>
      <ul>
        <li>by {{ comment.user.get_profile.display_name }}</li>
        <li>{{ comment.created|timesince }} ago</li>
      </ul>
      
      <ul class="right">
        {% if request.user == comment.user %}
        <li>
          <a id="edit-{{ comment.id }}" onclick="comment_edit(this, event)" href="#">Edit</a>
        </li>
        <li>
          <a id="delete-{{ comment.id }}" onclick="comment_delete(this, event)" href="#">Delete</a>
        </li>
        {% else %}
        <li>
          <a id="reply-{{ comment.id }}" onclick="comment_reply(this, event)" href="#">Reply</a>
        </li>
        {% endif %}
      </ul>
      
      {% if replies %}
        <div class="replies">
          {{ replies|safe }}
        </div>
      {% endif %}
    </div>

Notice the {{ replies }} subsitution. That is how the recursion is handled for the multi-level
commment replies.

Note: The js events are inline because I was not sure how to associate the events when the 
comment was inserted into the DOM. If you know how to do that with jquery please let me know.

#. Include the js where its needed

#. Debug. This is my first app so its going to be rough but there enough should be there to get 
you started. Hopefully it doesn't suck too bad. Good Luck!!

Email notifications
-------------------

Here is how you could support email notifications.::

    def comment_posted(sender, comment, request, **kwargs):
        from dakku import email_util

        for username, email in settings.ADMINS:
            email_util.send_email(
                email,
                'email/comment_was_posted.msg',
                comment=comment,
                settings=settings)

        logger.info('%s posted a comment' % (request.user))

    yacapp_signals.comment_was_posted.connect(comment_posted)
