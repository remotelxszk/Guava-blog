from django.contrib import admin

from blogs.models import BlogPost, PostComment
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(PostComment)