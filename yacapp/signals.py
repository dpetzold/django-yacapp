from django.dispatch import Signal

comment_was_posted = Signal(providing_args=["comment", "request"])
