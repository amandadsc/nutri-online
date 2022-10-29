from django.contrib import admin
from .models import Paciente, Consulta, PlanoAlimentar

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Consulta)
admin.site.register(PlanoAlimentar)