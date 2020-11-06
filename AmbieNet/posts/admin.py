"""Posts models admin."""

#Django
from django.contrib import admin

#Models
from AmbieNet.posts.models.posts import Post
from AmbieNet.posts.models.images import Image

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    """Post models admin."""
    list_display = ('id','title', 'description','latitud','longitud')
    list_filter = ('type_catastrophe','validator_number')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Image models admin."""
    list_display = ('id','post', 'photo')