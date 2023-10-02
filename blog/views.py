import django.contrib.auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from blog.forms import CommentForm, SignUpForm, PostSearchForm
from blog.models import Post, Tag, Comment, User


@login_required(login_url='/accounts/login/')
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponseRedirect(reverse("blog:post_list"))


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")
    template_name = "blog/post_list.html"
    paginate_by = 5

    def get_queryset(self):
        form = PostSearchForm(self.request.GET)

        queryset = Post.objects.select_related("user").prefetch_related("tags").order_by("-created_at")

        if form.is_valid():
            queryset = queryset.filter(title__icontains=form.cleaned_data["title"])

        if tag := self.request.GET.get("tag", ""):
            queryset = queryset.filter(tags__name=tag)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = PostSearchForm(
            initial={"title": title}
        )
        context["tag_list"] = Tag.objects.all()
        return context


@login_required(login_url='/accounts/login/')
def post_detail(request, pk):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post__id=pk).order_by("-created_at")
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


class SignUpView(LoginRequiredMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = get_user_model().objects.all()


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags")


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post


class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User


class UserDelete(LoginRequiredMixin, generic.DeleteView):
    model = User
