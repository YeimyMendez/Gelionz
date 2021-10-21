from django.shortcuts import render
from rest_framework import serializers
from aplicaciones.principal.models import *

# Create your views here.

class usuario_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Usuario
		fields = ('id','username','email','nombres','apellidos','documento','celular','genero','usuario_activo','rol_de_usuario','password')

class equipo_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Equipo
		fields = ('nombre_capitan','nombre_equipo','num_integrantes','eventos_jugados')

class userequipo_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = User_Equipo
		fields = ('equipo_FK','user')	

class evento_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Evento
		fields = ('tipo_evento','fecha_hora_evento','valor_evento','ganador_evento','cantidad_jugadores','estado','organizador')

class inscripcion_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Inscripcion
		fields = ('fecha_hora_inscripcion','es_ganador','is_paid','id_equipo_FK','inscripcion_evento_FK')

class pago_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Pago
		fields = ('tipo_pago','fecha_hora_pago','foto','valor_pago','estado_pago','id_evento_FK')