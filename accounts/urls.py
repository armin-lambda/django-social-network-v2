from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-create'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),

    path('reset-password/', views.UserPasswordResetView.as_view(), name='user-password-reset'),
    path('verify-code/', views.UserPasswordVerifyCodeView.as_view(), name='user-password-verify-code'),
    path('change-password/', views.UserPasswordChangeView.as_view(), name='user-password-change'),

    path('edit-user/', views.UserUpdateView.as_view(), name='user-update'),
    path('delete-user/', views.UserDeleteView.as_view(), name='user-delete'),
    path('delete-profile-image/', views.UserProfileImageDeleteView.as_view(), name='user-profile-image-delete'),

    path('', views.UserListView.as_view(), name='user-list'),

    path('<str:username>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<str:username>/follow/', views.UserFollowView.as_view(), name='user-follow'),
    path('<str:username>/unfollow/', views.UserUnfollowView.as_view(), name='user-unfollow'),
    path('<str:username>/followers/', views.UserFollowerListView.as_view(), name='user-follower-list'),
    path('<str:username>/following/', views.UserFollowingListView.as_view(), name='user-following-list')
]
