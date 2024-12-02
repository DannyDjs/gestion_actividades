from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView,CustomLogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='autenticacion/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='autenticacion/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='autenticacion/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='autenticacion/password_reset_complete.html'), name='password_reset_complete'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
