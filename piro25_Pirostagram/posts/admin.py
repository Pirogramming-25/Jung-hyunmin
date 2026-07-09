from django.contrib import admin
from .models import Post, PostImage, Like, Bookmark, Comment, Story, StoryImage

admin.site.register([Post, PostImage, Like, Bookmark, Comment, Story, StoryImage])
