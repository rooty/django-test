# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals


class Post(models.Model):
    title = models.CharField(max_length=60)
    short_body = models.TextField(max_length=255)
    body = models.TextField()
    comment_count = models.IntegerField(editable=False, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s: %s' % (self.post, self.author)


def countcommentonsave(sender, instance, created, **kwargs):
    post = instance.post
    post.comment_count = \
        Comment.objects.filter(post__id=post.id, confirmed=True).count()
    post.save()


def countcommentondelete(sender, instance, **kwargs):
    post = instance.post
    post.comment_count = \
        Comment.objects.filter(post__id=post.id, confirmed=True).count()
    post.save()


signals.post_save.connect(countcommentonsave, sender=Comment)
signals.post_delete.connect(countcommentondelete, sender=Comment)
