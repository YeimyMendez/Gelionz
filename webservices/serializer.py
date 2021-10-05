from django.shortcuts import render
from rest_framework import serializers
from aplicaciones.principal.models import *

# Create your views here.

class usuario_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model  = Usuario
		fields = ('username','nombres')