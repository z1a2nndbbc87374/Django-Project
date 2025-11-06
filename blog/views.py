from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.db.models import Q

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all()

    context = {
        "posts": posts,
        "categories": categories,
    }
    return render(request, "home.html", context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    categories = Category.objects.all()

    # Show approved comments for this post
    comments = post.comments.filter(is_public=True)

    context = {
        "post": post,
        "categories": categories,
        "comments": comments,
    }
    return render(request, "post_detail.html", context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, is_published=True)

    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "category_posts.html", context)

def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Comment.objects.create(
            post=post,
            name=name,
            email=email,
            message=message,
        )

        return redirect(post.get_absolute_url())

    return redirect(post.get_absolute_url())

def search(request):
    query = request.GET.get("q", "")

    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(excerpt__icontains=query)
    ).filter(is_published=True)

    context = {"posts": posts, "query": query}
    return render(request, "search.html", context)

