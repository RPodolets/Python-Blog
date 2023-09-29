from django.contrib import admin
from django.contrib.auth.models import Group

from blog.models import Post, Comment, Tag, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]
    list_filter = ["username"]
    ordering = ["date_joined"]


admin.site.unregister(Group)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
