from django.urls import path, include
from rest_framework import routers
from aplicaciones.principal.models import *
from webservices.views import *

router = routers.DefaultRouter()
router.register(r'usuario', usuario_viewset)

urlpatterns = [
	path('api/', include(router.urls)),
	path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]