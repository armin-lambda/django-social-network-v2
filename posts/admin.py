from django.contrib import admin

from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'created_at',
        'updated_at',
    ]
    list_filter = ['user', 'created_at']
    search_fields = [
        # User fields
        'user__username',
        'user__first_name',
        'user__last_name',
        
        # Post fields
        'title',
        'description',
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = [
        # User fields
        'user__username',
        'user__first_name',
        'user__last_name',
        
        # Post fields
        'post_title',
        'post_description',

        # Comment fields
        'body',
    ]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = [
        # User fields
        'user__username',
        'user__first_name',
        'user__last_name',
        
        # Post fields
        'post_title',
        'post_description',
    ]
