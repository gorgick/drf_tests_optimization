from django.contrib import admin

from blogs.models import Blog, Like, Comment

admin.site.register(Blog)
admin.site.register(Like)
admin.site.register(Comment)
