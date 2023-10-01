from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from blog.forms import CommentForm
from blog.models import Post, Tag, Comment


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_list"] = Tag.objects.all()
        print(context.keys())
        return context


def post_detail(request, pk):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post__id=pk)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            user = get_user_model().objects.get(id=request.user.id)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = user
            new_comment.save()
            return HttpResponseRedirect(f"/{pk}")

    comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form
    }
    return render(request, template_name, context=context)
