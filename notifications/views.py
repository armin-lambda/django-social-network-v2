from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.pagination import get_pagination_context
from .models import Notification


class NotificationListView(LoginRequiredMixin, View):
    template_name = 'notifications/notification-list.html'

    def get(self, request):
        notification_list = request.user.get_notification_list()
        return render(request, self.template_name, {
            'page_obj': get_pagination_context(request, notification_list, 10),
            'can_read_all': notification_list.filter(is_read=False).exists(),
        })


class NotificationReadView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        notification = get_object_or_404(Notification, pk=kwargs['pk'], to_user=request.user)

        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return redirect('notifications:notification-list')


class NotificationDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        get_object_or_404(Notification, pk=kwargs['pk'], to_user=request.user).delete()
        return redirect('notifications:notification-list')


class NotificationReadAllView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications:notification-list')


class NotificationDeleteAllView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.notifications.all().delete()
        return redirect('notifications:notification-list')

