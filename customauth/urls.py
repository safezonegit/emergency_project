from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='user_register'),
    path('login/',views.login_view, name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    # Password Reset
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Password Change (only when logged in)
    path("accounts/password_change/", auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name="password_change"),
    path("accounts/password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name="password_change_done"),
]