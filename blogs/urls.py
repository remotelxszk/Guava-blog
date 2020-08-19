"""Defines URL patterns for blogs."""
from django.conf.urls import url
from . import views

app_name = 'blogs'
urlpatterns = [
    #Home page
    url(r'^$', views.index, name='index'),
    #New post
    url(r'^new_post/$', views.new_post, name='new_post'),
    #Edit post
    url(r'^edit_post/(?P<post_id>\d+)/$', views.edit_post, name='edit_post'),
    #Delete post
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
    #View post
    url(r'^view_post/(?P<post_id>\d+)/$', views.view_post, name='view_post'),
    #New comment
    url(r'^new_comment/(?P<post_id>\d+)/$', views.new_comment, name='new_comment'),
    #Delete comment
    url(r'^delete_comment/(?P<post_id>\d+)/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    #Edit comment
    url(r'^edit_comment/(?P<post_id>\d+)/(?P<comment_id>\d+)/$', views.edit_comment, name='edit_comment'),
]