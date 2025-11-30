from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import Post


def blog_list_view(request):
    """
    Display all published blog posts with pagination
    """
    # Get search query
    query = request.GET.get('q', '')

    # Base queryset
    posts = Post.objects.filter(is_published=True).select_related('author')

    # Apply search filter if query exists
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )

    # Order by published date (newest first)
    posts = posts.order_by('-published_date')

    # Pagination (12 posts per page)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'website/blog_list.html', context)


def blog_detail_view(request, slug):
    """
    Display individual blog post with related posts
    """
    # Get the post or 404
    post = get_object_or_404(
        Post.objects.select_related('author'),
        slug=slug,
        is_published=True
    )

    # Increment view count (using F expression to avoid race conditions)
    from django.db.models import F
    Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
    post.refresh_from_db()  # Refresh to get updated view count

    # Get related posts (same author or recent posts, excluding current post)
    related_posts = Post.objects.filter(
        is_published=True
    ).exclude(
        pk=post.pk
    ).select_related('author').order_by('-published_date')[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }

    return render(request, 'website/blog_detail.html', context)