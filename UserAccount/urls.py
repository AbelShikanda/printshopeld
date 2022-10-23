from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm
from django.views.generic import TemplateView

app_name = 'UserAccount'
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html', form_class=UserLoginForm), name='login'),
    path('register', views.register_view, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    
    path('password_reset/',
                    auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                                                success_url='password_reset_email_confirm',
                                                                email_template_name='registration/password_reset_email.html',
                                                                form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', 
                    auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
                                                                success_url='/UserAccount/reset/done/', 
                                                                form_class=PwdResetConfirmForm),
                                                                name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
                    TemplateView.as_view(template_name="registration/password_reset_done.html"), 
                                                                name='password_reset_done'),
    path('reset/done', 
                    TemplateView.as_view(template_name="registration/password_reset_complete.html"), 
                                                                name='password_reset_complete'),
    
    path('accounts', views.accounts_view, name='accounts_view'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="user/delete_confirm.html"), name='delete_confirmation'),
]