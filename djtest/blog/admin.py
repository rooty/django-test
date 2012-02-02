# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Post, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    display_fields = ["post", "author", "created", "confirmed"]


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ]
    search_fields = ["title"]
    display_fields = ["title", "created", "comment_count", ]

admin.site.register(Post, PostAdmin)
