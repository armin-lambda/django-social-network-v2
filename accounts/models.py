from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField

from utils.paths import get_user_profile_image_upload_path
from utils.validators import UsernameValidator, NameValidator, URLValidator
from .managers import CustomUserManager


User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UsernameValidator()],
        help_text='Enter a unique username (letters, numbers, dot, or underline, up to 30 characters).',
        error_messages={
            'unique': 'This username already exists',
        },
    )
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        help_text='Enter a unique email.',
        error_messages={
            'unique': 'This email already exists',
        },
    )
    first_name = models.CharField(
        max_length=15,
        validators=[NameValidator('First name')],
        help_text='Enter a valid first name (letters, up to 15 characters).',
    )
    last_name = models.CharField(
        max_length=15,
        validators=[NameValidator('Last name')],
        help_text='Enter a valid last name (letters, up to 15 characters).',
    )
    phone_number = PhoneNumberField(
        unique=True,
        help_text='Enter your phone number in international format, e.g., +981234567890',
        error_messages={
            'unique': 'This phone number already exists',
        },
    )
    website_url = models.URLField(
        max_length=50,
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text='Enter a website url (https://, up to 50 characters).',
    )
    bio = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Enter your bio (up to 200 characters).',
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=get_user_profile_image_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
        help_text='Enter your profile image (png, jpg, jpeg, gif).',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    # ----- URLS -----
    def get_absolute_url(self):
        return reverse('accounts:user-detail', args=[self.username])
    
    def get_update_url(self):
        return reverse('accounts:user-update')
    
    def get_delete_url(self):
        return reverse('accounts:user-delete')
    
    def get_profile_image_delete_url(self):
        return reverse('accounts:user-profile-image-delete')
    
    def get_follow_url(self):
        return reverse('accounts:user-follow', args=[self.username])

    def get_unfollow_url(self):
        return reverse('accounts:user-unfollow', args=[self.username])

    def get_follower_list_url(self):
        return reverse('accounts:user-follower-list', args=[self.username])

    def get_following_list_url(self):
        return reverse('accounts:user-following-list', args=[self.username])

    def get_post_create_url(self):
        return reverse('posts:post-create')

    # ----- COUNTS -----
    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()
    
    def get_posts_count(self):
        return self.posts.count()
    
    def get_notifications_count(self):
        return self.notifications.filter(is_read=False).count()

    # ----- LISTS -----
    def get_follower_list(self):
        return CustomUser.objects.filter(following__to_user=self)

    def get_following_list(self):
        return CustomUser.objects.filter(followers__from_user=self)
    
    def get_post_list(self):
        return self.posts.all()
    
    def get_notification_list(self):
        return self.notifications.all()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f"{self.from_user.username} followed {self.to_user.username}"


