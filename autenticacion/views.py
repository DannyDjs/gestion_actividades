from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


class CustomLoginView(LoginView):
    template_name = 'autenticacion/login.html'  # Asegúrate de que este template exista
    success_url = reverse_lazy('dashboard')  # Cambia 'dashboard' por la URL a la que deseas redirigir

    def form_valid(self, form):
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')