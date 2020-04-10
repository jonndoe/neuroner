# this file to be removed after figuring out how to
# get blogIndexPage displaying blogs based on tag provided.


from django.http import HttpResponse
import datetime

from taggit.models import Tag
from django.contrib import messages




from django.shortcuts import redirect, render

from bakerydemo.blog.models import BlogIndexPage, BlogPage


def tag_archive(request, tag=None, page=None):

    print('request', request)
    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(tag=None):
        posts = BlogPage.objects.live()
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    try:
        tag = Tag.objects.get(slug=tag)
        print('tag is: ', tag)
    except Tag.DoesNotExist:
        if tag:
            msg = 'There are no blog posts tagged with "{}"'.format(tag)
            messages.add_message(request, messages.INFO, msg)
        return redirect('search')

    posts = get_posts(tag=tag)
    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'blog/blog_index_page.html', context)
