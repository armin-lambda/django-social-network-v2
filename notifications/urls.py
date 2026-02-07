from django.urls import path

from . import views


app_name = 'notifications'
urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('read/<int:pk>/', views.NotificationReadView.as_view(), name='notification-read'),
    path('delete/<int:pk>/', views.NotificationDeleteView.as_view(), name='notification-delete'),
    path('read-all/', views.NotificationReadAllView.as_view(), name='notification-read-all'),
    path('delete-all/', views.NotificationDeleteAllView.as_view(), name='notification-delete-all'),
]
