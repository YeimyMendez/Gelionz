from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
#URLS DE USUARIO  ANONIMO
	path('contacto', views.contacto, name="Contacto"),
    path('blog', views.blog, name="Blog"),
	path('login/', LoginView.as_view(template_name='login.html'), name='login'), #url de la vista login.
	path('register/', views.register, name='register'),#url de la vista Register
#URLS DE USUARIO JUGADOR
	path('perfil', views.perfil, name='perfil'), #url de la vista Perfil. 
    path('imgPerfil/', views.imgPerfil, name='imgPerfil'),
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
	path('lista_equipos/', views.lista_equipos, name = 'lista_equipos'),
	path('crear_equipo/', views.crear_equipo, name = 'crear_equipo'),
    # path('editarE/<int:id_evento>/', views.editarE_view, name = 'editarE_view'),
    # path('eliminarEvento/<int:id_evento>/', views.eliminarEvento_view, name = 'eliminarEvento_view'),
    path('detalle_equipo/<int:id_equipo>/', views.detalle_equipo, name = 'detalle_equipo_view'),
    path('listar_jugador/', views.listar_jugador, name = 'listar_jugador'),
    path('asociar_equipo/<int:id_equipo>/<int:id_jugador>/', views.asociar_equipo, name = 'asociar_equipo_view'),
    path('NivelCompetitivo', views.NivelCompetitivo, name="NivelCompetitivo"),
    path('seleccionar_equipo/<int:id_evento>/', views.seleccionar_equipo, name='seleccionar_equipo'),# mostrar MIS equipos a inscribir
    path('inscribirEquipo/<int:id_evento>/<int:id_equipo>/', views.inscribirEquipo, name='inscribirEquipo'),#url de la vista NIvel Competitivo
    
#URLS DEL STREAMER
	path('inicio/', views.inicio_view, name = 'inicio_view'),
	path('agregar_evento/', views.agregar_evento_view, name = 'agregar_evento_view'),
    path('listar_evento/<str:vista>/', views.listar_evento_view, name = 'listar_evento_view'),
    path('detalle/<int:id_evento>/', views.detalle_view, name = 'detalle_view'),
    path('editarE/<int:id_evento>/', views.editarE_view, name = 'editarE_view'),
    path('agregarG/<int:id_evento>/<int:id_equipo>/', views.agregarG_view, name = 'agregarG_view'),
    path('eliminarEvento/<int:id_evento>/', views.eliminarEvento_view, name = 'eliminarEvento_view'),
    path('pagos/', views.pagos_view, name = 'pagos_view')
]