from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from blog.forms import CommentForm, SignUpForm, PostSearchForm, UserForm, PostForm
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

        if form.is_valid():
            self.queryset = self.queryset.filter(title__icontains=form.cleaned_data["title"])

        if tag := self.request.GET.get("tag", ""):
            self.queryset = self.queryset.filter(tags__name=tag)

        return self.queryset

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

    if post:
        post.update_views()

    comments = Comment.objects.filter(post__id=pk).select_related("user").order_by("-created_at")
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            user = get_user_model().objects.get(id=request.user.id)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = user
            new_comment.save()
            return HttpResponseRedirect(reverse("blog:post_detail", kwargs={"pk": pk}))

    comment_form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form
    }
    return render(request, template_name, context=context)


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = get_user_model().objects.all()


class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse_lazy("blog:user_detail", kwargs={"pk": self.kwargs["pk"]})


class UserDelete(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("blog:index")


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    queryset = Post.objects.select_related("user").prefetch_related("tags")
    form_class = PostForm
    success_url = reverse_lazy("blog:post_list")


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post_list")


class CommentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self):
        post_id = Comment.objects.get(id=self.kwargs["pk"]).post.id
        return reverse_lazy("blog:post_detail", kwargs={"pk": post_id})
