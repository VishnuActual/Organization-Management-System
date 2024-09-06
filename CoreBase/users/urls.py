from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserUpdateAPIView, LogoutAPIView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # user urls
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('update/', UserUpdateAPIView.as_view(), name='update_profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
]
