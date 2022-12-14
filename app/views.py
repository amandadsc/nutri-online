from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Paciente, Consulta, PlanoAlimentar
from .forms import PacienteForm, ConsultaForm, PlanoAlimentarForm
from django.db.models import Q
from django.contrib import messages
from .decorators import usuario_nao_autenticado, usuarios_permitidos

# VIEWS AUTENTICACAO
@usuario_nao_autenticado
def entrar(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        try:
            usuario_aux = User.objects.get(email=email)
            usuario = authenticate(request, username=usuario_aux.username, password=senha)
            if usuario is not None:
                if usuario.groups.filter(name = 'admin'):
                    login(request, usuario)
                    messages.add_message(request, messages.SUCCESS, 'Admin logado com sucesso!')
                    return redirect('lista_paciente')
                else:
                    paciente = Paciente.objects.get(email=email)
                    login(request, usuario)
                    messages.add_message(request, messages.SUCCESS, 'Usuário logado com sucesso!')
                    return redirect('mostra_home', pk=paciente.pk)
            else:
                messages.add_message(request, messages.INFO, 'Senha digitada errada!')
                return HttpResponseRedirect('/')
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Usuário não cadastrado!')
            return HttpResponseRedirect('/')            
    return render(request, 'register/login.html', {'titulo': 'NutriOnline'})

@login_required(login_url='entrar')
def sair(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Deslogado com sucesso!')
    return HttpResponseRedirect('/')

@usuario_nao_autenticado
def confirma_email(request):
    if request.method == "POST":
        email = request.POST["emailConfirma"]
        try:
            usuario = get_object_or_404(User, email=email)
            paciente = get_object_or_404(Paciente, email=email)
            if usuario is not None:
                return redirect('redefine_senha', pk=paciente.pk)
        except:
            messages.add_message(request, messages.INFO, 'Usuário não encontrado!')
            return HttpResponseRedirect('/')

@usuario_nao_autenticado
def redefine_senha(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
            senha = request.POST['senha']
            atualizaUsuario = get_object_or_404(User, email=paciente.email)
            atualizaUsuario.password = senha
            atualizaUsuario.save()
            paciente.senha = senha
            paciente.save()
            messages.add_message(request, messages.SUCCESS, 'Senha atualizada com sucesso!')
            return redirect('entrar')                
    return render(request, 'register/redefine_senha.html', {'paciente': paciente, 'titulo': 'Redefinir Senha'})

# VIEWS DO NUTRICIONISTA/ADMIN
@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def lista_paciente(request):
    pacientes = Paciente.objects.all()
    return render(request, 'lista_paciente.html', {'pacientes': pacientes, 'titulo': 'NutriOnline'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def mostra_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'mostra_paciente.html', {'paciente': paciente, 'titulo':'NutriOnline'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def search(request):
    pacientes = []
    if request.method == "GET":
        query = request.GET.get('q')
        if query == '':
            query = 'None'
        pacientes = Paciente.objects.filter(Q(nome__icontains=query) |Q(cpf__iexact=query))
    return render(request, 'search.html', {'query': query, 'pacientes': pacientes})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def cadastra_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            try:
                usuario_aux = User.objects.get(email=request.POST['email'])
                if usuario_aux:
                    return render(request, 'edita_paciente.html',{'msg': 'Erro! Já existe um usuário com o mesmo e-mail'})
            except User.DoesNotExist:
                email = request.POST['email']
                usuario = request.POST['usuario']
                senha = request.POST['senha']
                novoUsuario = User.objects.create_user(username=usuario, email=email, password=senha)
                novoUsuario.save()
                paciente = form.save(commit=False)
                paciente.save()

                group = Group.objects.get(name='paciente')
                novoUsuario.groups.add(group)

                messages.add_message(request, messages.SUCCESS, 'Paciente cadastrado com sucesso!')
                return redirect('nova_consulta', pk=paciente.pk)
    else:
        form = PacienteForm()
    return render(request, 'edita_paciente.html', {'form': form, 'titulo': 'Cadastro de Paciente'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def edita_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            email = request.POST['email']
            usuario = request.POST['usuario']
            senha = request.POST['senha']
            atualizaUsuario = get_object_or_404(User, email=paciente.email)
            atualizaUsuario.username=usuario
            atualizaUsuario.email=email
            atualizaUsuario.password=senha
            atualizaUsuario.save()
            paciente = form.save(commit=False)
            paciente.save()
            messages.add_message(request, messages.SUCCESS, 'Paciente atualizado com sucesso!')
            return redirect('mostra_paciente', pk=paciente.pk)                
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'edita_paciente.html', {'form': form, 'paciente': paciente, 'titulo': 'Atualização de Paciente'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def exclui_paciente(request, pk):
    try:
        paciente = get_object_or_404(Paciente, pk=pk)
        usuario = get_object_or_404(User, email=paciente.email)
        paciente.delete()
        usuario.delete()
        messages.add_message(request, messages.SUCCESS, 'Paciente excluído com sucesso!')
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Usuário não existe')
        return redirect ('lista_paciente')
    except Exception as e: 
        return redirect(request, 'lista_paciente',{'err':e.message})
    return redirect ('lista_paciente')
    
    
@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])    
def nova_consulta(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            messages.add_message(request, messages.SUCCESS, 'Consulta criada com sucesso!')
            return redirect('mostra_paciente', pk=paciente.pk)
    else:
        form = ConsultaForm()
    return render(request, 'nova_consulta.html', {'form': form, 'paciente':paciente, 'titulo': 'Nova Consulta'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def edita_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    paciente = consulta.paciente
    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            messages.add_message(request, messages.SUCCESS, 'Consulta atualizada com sucesso!')
            return redirect('lista_consulta', pk=paciente.pk)
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'nova_consulta.html', {'form': form, 'paciente':paciente, 'consulta': consulta, 'titulo': 'Atualiza Consulta'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def exclui_consulta(request, pk):
    try:
        consulta = get_object_or_404(Consulta, pk=pk)
        paciente = consulta.paciente
        consulta.delete()
        print("excluindo")
        messages.add_message(request, messages.SUCCESS, 'Consulta excluída com sucesso!')
    except Exception: 
        messages.add_message(request, messages.ERROR, 'Não foi possível excluir consulta!')
        return redirect(request, 'lista_consulta')
    return redirect ('lista_consulta', pk=paciente.pk)
    

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def novo_plano_alimentar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        form = PlanoAlimentarForm(request.POST)
        if form.is_valid():
            plano_alimentar = form.save(commit=False)
            plano_alimentar.paciente = paciente
            plano_alimentar.save()
            messages.add_message(request, messages.SUCCESS, 'Plano Alimentar criado com sucesso!')
            return redirect('novo_plano_alimentar', pk=paciente.pk)
    else:
        form = PlanoAlimentarForm()
    return render(request, 'novo_plano_alimentar.html', {'form': form, 'paciente':paciente, 'titulo': 'Novo Plano Alimentar'})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin'])
def edita_plano_alimentar(request, pk, dia_da_semana):
    paciente = get_object_or_404(Paciente, pk=pk)
    plano_alimentar = get_object_or_404(PlanoAlimentar, paciente=paciente, dia_da_semana=dia_da_semana)
    if request.method == "POST":
        form = PlanoAlimentarForm(request.POST, instance=plano_alimentar)
        if form.is_valid():
            plano_alimentar = form.save(commit=False)
            plano_alimentar.paciente = paciente
            plano_alimentar.save()
            messages.add_message(request, messages.SUCCESS, 'Plano Alimentar atualizado com sucesso!')
            return redirect('plano_alimentar', pk=paciente.pk)
    else:
        form = PlanoAlimentarForm(instance=plano_alimentar)  
    return render(request, 'novo_plano_alimentar.html', {'form': form, 'paciente':paciente, 'plano_alimentar': plano_alimentar, 'titulo': 'Atualiza Plano Alimentar'})


# VIEWS DO PACIENTE
@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['paciente'])
def mostra_home(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'home.html', {'paciente': paciente, 'titulo': 'NutriOnline'})


# VIEWS COMUNS
@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin', 'paciente'])
def evolucao_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    group = request.user.groups.all()[0].name
    if group == 'admin':
        titulo = 'Evolução do Paciente'
    else:
        titulo = 'Minha Evolução'
    return render(request, 'evolucao.html', {'paciente': paciente, 'titulo': titulo, 'group': group})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin', 'paciente'])
def dados_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    consulta = Consulta.objects.filter(paciente=paciente).last()
    idade = paciente.calcula_idade()
    group = request.user.groups.all()[0].name
    if group == 'admin':
        titulo = 'Dados do Paciente'
    else:
        titulo = 'Meus Dados Pessoais'
    return render(request, 'dados_paciente.html', {'paciente': paciente, 'consulta': consulta, 'idade': idade, 'titulo': titulo, 'group': group})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin', 'paciente'])
def plano_alimentar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    plano_alimentar = PlanoAlimentar.objects.filter(paciente=paciente) 
    group = request.user.groups.all()[0].name
    if group == 'admin':
        titulo = 'Plano Alimentar Atual'
    else:
        titulo = 'Meu Plano Alimentar'
    return render(request, 'plano_alimentar.html', {'paciente':paciente, 'plano_alimentar': plano_alimentar, 'titulo': titulo, 'group': group})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin', 'paciente'])
def lista_consulta(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    consultas = Consulta.objects.filter(paciente=paciente).order_by('-data')
    group = request.user.groups.all()[0].name 
    if group == 'admin':
        titulo = 'Consultas'
    else:
        titulo = 'Minhas Consultas'
    return render(request, 'lista_consulta.html', {'consultas': consultas, 'paciente': paciente, 'group': group, 'titulo': titulo})

@login_required(login_url='entrar')
@usuarios_permitidos(roles_permitidos=['admin', 'paciente'])
def consulta(request, pk):
    consulta =  get_object_or_404(Consulta, pk=pk)
    data = consulta.data.date()
    paciente = consulta.paciente
    idade = paciente.calcula_idade()
    group = request.user.groups.all()[0].name
    return render(request, 'consulta.html', {'consulta': consulta, 'paciente': paciente, 'idade': idade, 'data': data, 'group': group, 'titulo': 'Consultas'})


@login_required(login_url='entrar')
def grafico_peso(request, pk):
    datas = []
    pesos = []
    paciente = get_object_or_404(Paciente, pk=pk)
    queryset = Consulta.objects.filter(paciente=paciente).order_by('data')
    for consulta in queryset:
        consulta.data = consulta.data.date()
        datas.append(consulta.data)
        pesos.append(consulta.peso)
    data_json = {
        'datas': datas,
        'pesos': pesos,
    }
    return JsonResponse(data_json)

@login_required(login_url='entrar')
def grafico_massa_gordura(request, pk):
    datas = []
    massa_gordura = []
    paciente = get_object_or_404(Paciente, pk=pk)
    queryset = Consulta.objects.filter(paciente=paciente).order_by('data')
    for consulta in queryset:
        consulta.data = consulta.data.date()
        datas.append(consulta.data)
        massa_gordura.append(consulta.massa_gordura)
    data_json = {
        'datas': datas,
        'massa_gordura': massa_gordura,
    }
    return JsonResponse(data_json)

@login_required(login_url='entrar')
def grafico_massa_muscular(request, pk):
    datas = []
    massa_muscular = []
    paciente = get_object_or_404(Paciente, pk=pk)
    queryset = Consulta.objects.filter(paciente=paciente).order_by('data')
    for consulta in queryset:
        consulta.data = consulta.data.date()
        datas.append(consulta.data)
        massa_muscular.append(consulta.massa_muscular)
    data_json = {
        'datas': datas,
        'massa_muscular': massa_muscular,
    }
    return JsonResponse(data_json)

@login_required(login_url='entrar')
def grafico_imc(request, pk):
    datas = []
    imc = []
    paciente = get_object_or_404(Paciente, pk=pk)
    queryset = Consulta.objects.filter(paciente=paciente).order_by('data')
    for consulta in queryset:
        consulta.data = consulta.data.date()
        datas.append(consulta.data)
        imc.append(consulta.imc_valor)
    data_json = {
        'datas': datas,
        'imc': imc,
    }
    return JsonResponse(data_json)    

def handler_404(request, exception):
    return render(request, 'error/erro_404.html')