from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from blog.models import Post


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")
    template_name = "blog/index.html"
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")
