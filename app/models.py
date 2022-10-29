from datetime import date
from django.utils import timezone
from django.db import models

# Create your models here.
class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    usuario = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=12)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=50)
    objetivo = models.CharField(max_length=400)
    cadastrado_em = models.DateTimeField(default=timezone.now)

    def calcula_idade(self):
        hoje = date.today().year
        return hoje - self.data_nascimento.year

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    paciente = models.ForeignKey('app.Paciente', on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    peso = models.DecimalField(max_digits=4, decimal_places=1)
    altura = models.DecimalField(max_digits=3, decimal_places=2)
    imc_valor = models.DecimalField(max_digits=4, decimal_places=2)
    imc_classificacao = models.CharField(max_length=10)
    massa_gordura = models.DecimalField(max_digits=4, decimal_places=1)
    massa_muscular = models.DecimalField(max_digits=4, decimal_places=1)
    gordura_visceral = models.DecimalField(max_digits=4, decimal_places=1)
    medida_braco_esq = models.DecimalField(max_digits=4, decimal_places=1)
    medida_braco_dir = models.DecimalField(max_digits=4, decimal_places=1)
    medida_perna_esq = models.DecimalField(max_digits=4, decimal_places=1)
    medida_perna_dir = models.DecimalField(max_digits=4, decimal_places=1)
    medida_abdomem = models.DecimalField(max_digits=4, decimal_places=1)
    medida_quadril = models.DecimalField(max_digits=4, decimal_places=1)
    medida_cintura = models.DecimalField(max_digits=4, decimal_places=1)
    medida_peito = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"{self.paciente.nome}, {self.data}"

class PlanoAlimentar(models.Model):
    paciente = models.ForeignKey('app.Paciente', on_delete=models.CASCADE)

    dia_da_semana_choices = [
        ('Segunda', 'SEG'),
        ('Terça', 'TER'),
        ('Quarta', 'QUA'),
        ('Quinta', 'QUI'),
        ('Sexta', 'SEX'),
        ('Sábado', 'SAB'),
        ('Domingo', 'DOM'),
    ]
    dia_da_semana = models.CharField(max_length=7, choices=dia_da_semana_choices)

    cafe_da_manha = models.TextField()
    lanche_da_manha = models.TextField()
    almoco = models.TextField()
    lanche_da_tarde = models.TextField()
    jantar = models.TextField()
    ceia = models.TextField()

    def __str__(self):
        return f"{self.paciente.nome}, {self.dia_da_semana}"
