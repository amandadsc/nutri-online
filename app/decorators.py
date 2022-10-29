from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Paciente 

def usuario_nao_autenticado(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name = 'admin'):
                return redirect('lista_paciente')
            else:
                email = request.user.email
                paciente = get_object_or_404(Paciente, email=email)
                return redirect('mostra_home', pk=paciente.pk)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def usuarios_permitidos(roles_permitidos=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in roles_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Você não está atutorizado a ver essa página!")
        return wrapper_func
    return decorator