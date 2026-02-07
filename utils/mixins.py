from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()


class AnonymousRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:post-list')
        return super().dispatch(request, *args, **kwargs)


class SelfForbiddenMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        if request.user == user:
            return redirect(request.user.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)
