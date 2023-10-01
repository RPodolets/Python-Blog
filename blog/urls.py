from django.urls import path

from blog.views import PostListView, post_detail

urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path("<int:pk>/", post_detail, name="post_detail")
]

app_name = "blog"
