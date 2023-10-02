from django.urls import path

from blog.views import (
    PostListView,
    post_detail,
    SignUpView,
    UserDetailView,
    PostUpdateView,
    PostDeleteView,
    UserUpdate,
    UserDelete,
    index,
    CommentDelete,
)

urlpatterns = [
    path("", index, name="index"),
    path("post/", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post_delete"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/update", UserUpdate.as_view(), name="user_update"),
    path("user/<int:pk>/delete", UserDelete.as_view(), name="user_delete"),
    path("comment/<int:pk>/delete", CommentDelete.as_view(), name="comment_delete"),
    path("signup/", SignUpView.as_view(), name="signup")
]

app_name = "blog"
