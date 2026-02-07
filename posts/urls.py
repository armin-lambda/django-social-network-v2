from django.urls import path

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('new/', views.PostCreateView.as_view(), name='post-create'),
    
    path('edit-post/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    path('delete-post/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    path('<int:pk>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', views.PostUnlikeView.as_view(), name='post-unlike'),
]
