from aplicaciones.principal.models import *
from .serializer import *
from rest_framework import viewsets

# API USUARIO
class usuario_viewset(viewsets.ModelViewSet):
	queryset = Usuario.objects.all()
	serializer_class = usuario_serializer

# API EQUIPO
class equipo_viewset(viewsets.ModelViewSet):
	queryset = Equipo.objects.all()
	serializer_class = equipo_serializer 

# API USER QUIPO
class userequipo_viewset(viewsets.ModelViewSet):
	queryset = User_Equipo.objects.all()
	serializer_class = userequipo_serializer

# API USER EVENTO
class evento_viewset(viewsets.ModelViewSet):
	queryset = Evento.objects.all()
	serializer_class = evento_serializer
	
# API USER INSCRIPCION
class pago_viewset(viewsets.ModelViewSet):
	queryset = Pago.objects.all()
	serializer_class = pago_serializer