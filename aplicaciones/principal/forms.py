
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from . models import Equipo, Inscripcion, Post, Usuario, Evento

# SUBIR IMAGEN DE PERFIL
class ImgPerfilForm(forms.ModelForm):
	# imagen = forms.ImageField(required=False, widget=forms.FileInput)
	class Meta:
		model = Usuario
		fields = ['imagen','username']		

# Formulario registro
class UserRegisterForm(UserCreationForm):
	password1 = forms.CharField(label='Contraseña',widget= forms.PasswordInput)
	password2 = forms.CharField(label='Confirmar Contraseña',widget= forms.PasswordInput)
	
	class Meta:
		model      = Usuario
		fields     = ['username','nombres','apellidos','email','rol_de_usuario','password1','password2']
		help_texts = {k:"" for k in fields }

# Formulario Inscrpciones
class form_inscripcion(forms.ModelForm):
	class Meta:
		model   = Inscripcion
		fields  = '__all__'
		exclude = ['es_ganador']

class form_crear_equipo(forms.ModelForm):
	class Meta:
		model   = Equipo
		fields  = '__all__'
		exclude = ['eventos_jugados', 'num_integrantes']

# Formulario publicaciones
class PostForm(forms.ModelForm):
	content    = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': '¿Qué está pasando?'}), required=True)
	class Meta:
		model  = Post
		fields = ['content']

class form_agregar_evento(forms.ModelForm):
	class Meta:
		model   = Evento
		fields  = '__all__'
		exclude = ['ganador_evento', 'is_paid', 'organizador', 'estado']
		widgets = {'fecha_hora_evento':forms.DateTimeInput(attrs={'type': 'date'})}		
		
class FormularioContacto(forms.Form):
		nombre    = forms.CharField(label="Nombre", required=True)
		email     = forms.CharField(label="Email", required=True)
		contenido = forms.CharField(label="Contenido", widget=forms.Textarea)

		fields  = ['nombre', 'email', 'contenido']
		widgets = {
			'nombre'    : forms.TextInput(attrs={'Placeholder':'Nombre'}),
			'email'     : forms.TextInput(attrs={'Placeholder':'Email'}),
			
		}

		""" labels = {
			'nombre':'Nombre',
			'email':'Email',
			'contenido':'Contenido',
		} """
