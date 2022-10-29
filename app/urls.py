from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('pacientes/', views.lista_paciente, name='lista_paciente'),
    path('pacientes/novo', views.cadastra_paciente, name='cadastra_paciente'), 
    path('pacientes/<int:pk>/edita', views.edita_paciente, name='edita_paciente'), 
    path('pacientes/<pk>/exclui', views.exclui_paciente, name='exclui_paciente'),    
    path('pacientes/<int:pk>/consulta', views.nova_consulta, name='nova_consulta'),
    path('search/', views.search, name='search'),
    path('pacientes/<int:pk>/dados', views.dados_paciente, name='dados_paciente'),
    path('pacientes/<int:pk>/detalhe', views.mostra_paciente, name='mostra_paciente'),
    path('pacientes/<int:pk>/plano_alimentar/novo', views.novo_plano_alimentar, name='novo_plano_alimentar'),
    path('pacientes/<int:pk>/plano_alimentar', views.plano_alimentar, name='plano_alimentar'),
    path('pacientes/<int:pk>/plano_alimentar/<dia_da_semana>/edita', views.edita_plano_alimentar, name='edita_plano_alimentar'),
    path('pacientes/<int:pk>/evolucao', views.evolucao_paciente, name='evolucao_paciente'),
    path('pacientes/<int:pk>/grafico_peso', views.grafico_peso, name='grafico_peso'),
    path('pacientes/<int:pk>/grafico_massa_gordura', views.grafico_massa_gordura, name='grafico_massa_gordura'),
    path('pacientes/<int:pk>/grafico_massa_muscular', views.grafico_massa_muscular, name='grafico_massa_muscular'),
    path('pacientes/<int:pk>/grafico_imc', views.grafico_imc, name='grafico_imc'),
    path('<int:pk>/home', views.mostra_home, name='mostra_home'),
    path('<int:pk>/dados_pessoais', views.dados_pessoais, name='dados_pessoais'),
    path('<int:pk>/plano_alimentar', views.plano_alimentar_atual, name='plano_alimentar_atual'),
    path('<int:pk>/evolucao', views.evolucao, name='evolucao'),
    path('confirma_email/', views.confirma_email, name='confirma_email'),
    path('<int:pk>/redefine_senha/', views.redefine_senha, name='redefine_senha'),
]
