from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator

from utils.paths import get_post_file_upload_path


User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
    )
    file = models.FileField(
        upload_to=get_post_file_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=[
                # Images
                'png',
                'jpg',
                'jpeg',
                'gif',

                # Videos
                'mp4',
                'mov',
                'avi',
                'mkv',
                'webm',
            ]),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.get_short_title()
    
    def get_short_title(self):
        return f"{self.title[:20]}..." if len(self.title) > 20 else self.title
    
    def file_is_image(self):
        return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    
    def file_is_video(self):
        return self.file.name.lower().endswith(('mp4', 'mov', 'avi', 'mkv', 'webm'))
    
    # ----- URLS -----
    def get_absolute_url(self):
        return reverse('posts:post-detail', args=[self.pk])
    
    def get_update_url(self):
        return reverse('posts:post-update', args=[self.pk])
    
    def get_delete_url(self):
        return reverse('posts:post-delete', args=[self.pk])
    
    def get_like_url(self):
        return reverse('posts:post-like', args=[self.pk])
    
    def get_unlike_url(self):
        return reverse('posts:post-unlike', args=[self.pk])
    
    # ----- COUNTS -----
    def get_comments_count(self):
        return self.comments.count()
    
    def get_likes_count(self):
        return self.likes.count()

    # ----- LISTS -----
    def get_comment_list(self):
        return self.comments.all()
    
    def get_like_list(self):
        return self.likes.all()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.post.get_short_title()} - {self.get_short_body()}" if len(self.body) > 20 else self.body

    def get_short_body(self):
        return f"{self.body[:20]}..." if len(self.body) > 20 else self.body


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} liked {self.post.get_short_title()}"
