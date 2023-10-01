from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from blog.models import Post, Tag


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")
    template_name = "blog/index.html"
    paginate_by = 5

    def get_queryset(self):
        if tag := self.request.GET.get("tag", ""):
            return Post.objects.filter(
                tags__name=tag
            ).select_related("user").prefetch_related().order_by("-created_at")
        return Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")
