from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Relation
from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_staff',
    ]
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'website_url',
        'bio',
    ]

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Personal Info', {
                'fields': (
                    'phone_number',
                    'image',
                    'website_url',
                    'bio',
                ),
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Personal Info', {
                'fields': (
                    'phone_number',
                    'image',
                    'website_url',
                    'bio',
                ),
            },
        ),
    )


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'from_user',
        'to_user',
        'created_at',
    ]
    list_filter = ['from_user', 'to_user', 'created_at']
    search_fields = [
        # from_user
        'from_user__username',
        'from_user__email',
        'from_user__first_name',
        'from_user__last_name',
        'from_user__phone_number',
        'from_user__website_url',
        'from_user__bio',

        # to_user
        'to_user__username',
        'to_user__email',
        'to_user__first_name',
        'to_user__last_name',
        'to_user__phone_number',
        'to_user__website_url',
        'to_user__bio',
    ]
