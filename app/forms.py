from django import forms
from .models import Consulta, Paciente, PlanoAlimentar

class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ('nome', 'email', 'usuario', 'senha', 'cpf', 'telefone', 'data_nascimento', 'genero', 'objetivo',)
        widgets= {
            'data_nascimento': forms.DateInput(format=('%Y-%m-%d'),)
        }

class ConsultaForm(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = ('peso', 'altura', 'imc_valor', 'imc_classificacao', 'massa_gordura', 'massa_muscular', 'gordura_visceral', 'medida_braco_esq', 'medida_braco_dir', 'medida_perna_esq', 'medida_perna_dir', 'medida_abdomem', 'medida_quadril', 'medida_cintura', 'medida_peito',)

class PlanoAlimentarForm(forms.ModelForm):

    class Meta:
        model = PlanoAlimentar
        fields = ('dia_da_semana', 'cafe_da_manha', 'lanche_da_manha', 'almoco', 'lanche_da_tarde', 'jantar', 'ceia',)

    def __init__(self, *args, **kwargs):
        super(PlanoAlimentarForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['dia_da_semana'].widget.attrs['disabled'] = True

    def clean_dia_da_semana(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.dia_da_semana
        else:
            return self.cleaned_data['dia_da_semana']