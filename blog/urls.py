from django.urls import path

from blog.views import PostListView, post_detail, SignUpView

urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path("<int:pk>/", post_detail, name="post_detail"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

app_name = "blog"
