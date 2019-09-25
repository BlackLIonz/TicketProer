from django.contrib import admin

from apps.feedbacks.models import Comment, Review


admin.site.register(Comment)
admin.site.register(Review)
