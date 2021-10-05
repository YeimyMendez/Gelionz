from aplicaciones.principal.models import *
from .serializer import *
from rest_framework import viewsets

class usuario_viewset(viewsets.ModelViewSet):
	queryset = Usuario.objects.all()
	serializer_class = usuario_serializer        
