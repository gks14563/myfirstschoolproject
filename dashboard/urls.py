from django.urls import path, re_path, include
from django.conf.urls import url

from dashboard.views import ExampleSecretView
from . import views
from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import LoginView
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r"^serve_ajax_request/$", views.serve_ajax_request),
    path('', views.index, name='index'),
    url(r'session_security/', include('session_security.urls')),
    path('register/', views.signup, name='register'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/kyc/uploads/', views.kyc_upload, name='kyc_form_upload'),
    path('dashboard/two_factor', views.two_factor, name='two_factor'),
    path('dashboard/', include(tf_urls), name='account'),
    path('dashboard/', include(tf_twilio_urls), name='twilio'),
    path('secret/',ExampleSecretView.as_view(), name='secret'), 
    path('send/',views.send, name ='send'),
    path('blog/',views.blog, name ='blog'),
    url(r'^reset/$',auth_view.PasswordResetView.as_view(template_name='dashboard/password_reset.html',
        email_template_name='dashboard/password_reset_email.html',subject_template_name='dashboard/password_reset_subject.txt'),
    name='password_reset'),
    url(r'^reset/done/$',auth_view.PasswordResetDoneView.as_view(template_name='dashboard/password_reset_done.html'),
    name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_view.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',auth_view.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_complete.html'),
    name='password_reset_complete'),
    url(r'^settings/password/$', auth_view.PasswordChangeView.as_view(template_name='dashboard/password_change.html'),
    name='password_change'),
    url(r'^settings/password/done/$', auth_view.PasswordChangeDoneView.as_view(template_name='dashboard/password_change_done.html'),
    name='password_change_done'),
    path('alpha/beta/gama/data', views.admin_image, name='admin_image'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

