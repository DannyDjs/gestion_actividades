import threading

# Variable global para almacenar el usuario
_user = threading.local()

class CurrentUserMiddleware:
    """
    Middleware para guardar el usuario actual en una variable global accesible.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user  # Almacena el usuario autenticado
        response = self.get_response(request)
        return response

def get_current_user():
    """
    Retorna el usuario actual almacenado en el middleware.
    """
    return getattr(_user, 'value', None)
