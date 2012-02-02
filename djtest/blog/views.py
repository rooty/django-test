from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.conf import settings

from .models import Post, Comment
from .forms import CommentForm


def post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post, confirmed=True)
    d = dict(
        post=post,
        comments=comments,
        form=CommentForm(),
        user=request.user
    )
    d.update(csrf(request))
    return render_to_response("blog/post.html", d)


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            newcomment = comment.save(commit=False)
            newcomment.post = post
            newcomment.save()
            return HttpResponseRedirect('/%s/' % pk)
    else:
        comment = CommentForm(request.POST, instance=comment)
    comments = Comment.objects.filter(post=post, confirmed=True)
    d = dict(post=post, comments=comments, form=comment)
    d.update(csrf(request))
    return render_to_response("blog/post.html", d)


def main(request):
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("blog/list.html",
        dict(
            posts=posts,
            post_list=posts.object_list
        )
    )
