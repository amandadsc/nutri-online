# Generated by Django 3.2.16 on 2022-10-29 20:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('usuario', models.CharField(max_length=50, unique=True)),
                ('senha', models.CharField(max_length=30)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('telefone', models.CharField(max_length=12)),
                ('data_nascimento', models.DateField()),
                ('genero', models.CharField(max_length=50)),
                ('objetivo', models.CharField(max_length=400)),
                ('cadastrado_em', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PlanoAlimentar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_da_semana', models.CharField(choices=[('Segunda', 'SEG'), ('Terça', 'TER'), ('Quarta', 'QUA'), ('Quinta', 'QUI'), ('Sexta', 'SEX'), ('Sábado', 'SAB'), ('Domingo', 'DOM')], max_length=7)),
                ('cafe_da_manha', models.TextField()),
                ('lanche_da_manha', models.TextField()),
                ('almoco', models.TextField()),
                ('lanche_da_tarde', models.TextField()),
                ('jantar', models.TextField()),
                ('ceia', models.TextField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('peso', models.DecimalField(decimal_places=1, max_digits=4)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=3)),
                ('imc_valor', models.DecimalField(decimal_places=2, max_digits=4)),
                ('imc_classificacao', models.CharField(max_length=10)),
                ('massa_gordura', models.DecimalField(decimal_places=1, max_digits=4)),
                ('massa_muscular', models.DecimalField(decimal_places=1, max_digits=4)),
                ('gordura_visceral', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_braco_esq', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_braco_dir', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_perna_esq', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_perna_dir', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_abdomem', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_quadril', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_cintura', models.DecimalField(decimal_places=1, max_digits=4)),
                ('medida_peito', models.DecimalField(decimal_places=1, max_digits=4)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.paciente')),
            ],
        ),
    ]
