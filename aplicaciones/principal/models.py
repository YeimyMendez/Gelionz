from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import CharField
from django.utils import timezone

# Personalizacion de user.

#Tabla de  Modificar  el Usuario Base
class UsuarioManager(BaseUserManager):
	def create_user(self, email, username, nombres, apellidos, password = None):
		if not email:
			raise ValueError('El usuario debe tener un correo electronico')
		usuario = self.model(
			username   = username,
			email      = self.normalize_email(email),
			nombres    = nombres,
			apellidos  = apellidos,
		)
		usuario.set_password(password)
		usuario.save()
		return usuario

	def create_superuser(self, username, email, nombres, apellidos, password):
		usuario = self.create_user(
			email,
			username  = username,
			nombres   = nombres,
			apellidos = apellidos,
			password  = password,
		)
		usuario.usuario_administrador = True
		usuario.save()
		return usuario

#Tabla usuario Personalizado
rol_usuario = (
	('jugador', 'Jugador'),
	('streaming', 'Streaming')
)

elegir_genero = (
	('femenino', 'Femenino'),
	('masculino', 'Masculino'),
	('otro', 'Otro')
)

class Usuario(AbstractBaseUser):
	username                = models.CharField('Nombre de usuario', unique = True, max_length=100)
	email                   = models.EmailField('Correo Electronico', max_length=254, unique=True)
	nombres                 = models.CharField('Nombres', max_length=200,blank=True, null=True)
	apellidos               = models.CharField('Apellidos', max_length=15,blank=True, null=True)
	documento               = models.CharField('Numero de documento', max_length=15,blank=True, null= True)
	celular                 = models.CharField('Numero de telefono', max_length=10,blank=True, null= True)
	genero                  = models.CharField('Genero', max_length=200, choices=elegir_genero)
	imagen                  = models.ImageField('imagen de perfil', upload_to='perfil/', max_length=200, blank=True, null=True)
	usuario_activo          = models.BooleanField(default=True)
	usuario_administrador   = models.BooleanField(default=False)
	rol_de_usuario          = models.CharField(max_length=200, choices=rol_usuario,default='jugador')
	objects                 = UsuarioManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS =['email','nombres','apellidos']

	def __str__(self):
		return f'{self.nombres} {self.apellidos}'

	def has_perm(self,perm,obj = None):
		return True

	def has_module_perms(self,app_label):
		return True

	@property
	def is_staff(self):
		return self.usuario_administrador


#Tabla Post
class Post(models.Model):
	user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='posts')
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.TextField()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f'{self.user.username}: {self.content}'		

#Tabla Cuenta

class Cuenta(models.Model):
	num_cuenta      =models.IntegerField()
	tipo_cuenta     =models.CharField(max_length=11)
	entidad         =models.CharField(max_length=80)
	perfil_FK       =models.ForeignKey(Usuario, on_delete=models.PROTECT)
	
	def __str__ (self):
		return self.num_cuenta
	
#Tabla Equipo

class Equipo(models.Model):  
	nombre_capitan  =models.CharField(max_length=80, null=True, blank=True)
	nombre_equipo   =models.CharField(max_length=80)
	num_integrantes =models.IntegerField(null=True, blank=True)
	eventos_jugados =models.CharField(max_length=200, default=0) #IntegerField
	
	def __str__ (self):
		return self.nombre_capitan + ' ' + self.nombre_equipo
#Tabla User_Equipo

class User_Equipo(models.Model):    
	equipo_FK   =models.ForeignKey(Equipo, on_delete=models.CASCADE)
	user     =models.ForeignKey(Usuario, on_delete=models.CASCADE)
	
	def __str__ (self):
		return self.user.username + self.equipo_FK.nombre_capitan

#Tabla Evento    
tipos_eventos = (
	('partida','partida'),
	('torneo','Torneo'),
	)
estados = (
	('disponible','Disponible'),
	('cancelado','Cancelado'),
	('reportado','Reportado'),
	('terminado','Terminado'),
	)

class Evento(models.Model):
	tipo_evento         =models.CharField(max_length=200, choices=tipos_eventos)
	codigo 		        =models.CharField(max_length=200, null=True, blank=True)
	fecha_hora_evento   =models.DateTimeField()
	valor_evento        =models.PositiveIntegerField() 
	ganador_evento      =models.CharField(max_length=200, null=True, blank=True)
	cantidad_jugadores  =models.PositiveIntegerField() #cant_equipos
	is_paid             =models.BooleanField(default=False) #si el evento fue pago al ganador
	estado              =models.CharField(max_length=200, choices=estados, default='disponible')
	organizador         =models.ForeignKey(Usuario, on_delete=models.CASCADE)
	
	def __str__ (self):
		return str(self.id)+' '+self.tipo_evento  
		#+' '+self.organizador.nombre_perfil
	
	#Tabla Inscrpcion

estados_equipo =(
	('inscrito','inscrito'),
	('ganador','ganador'),
	('perdedor','perdedor'),
	('pendiente','pendiente'),
)
class Inscripcion(models.Model):
	fecha_hora_inscripcion  =models.DateTimeField(auto_now_add=True)
	es_ganador              =models.CharField(max_length=50, choices=estados_equipo, default='inscrito') 
	pago                    =models.ImageField('imagen del pago', upload_to='pagos/', blank=True, null=True)
	id_equipo_FK            =models.ForeignKey(Equipo, on_delete=models.CASCADE)
	inscripcion_evento_FK   =models.ForeignKey(Evento, on_delete=models.CASCADE)
	
	def __str__ (self):
		return str(self.id)+' '+str(self.id_equipo_FK.id)+' '+str(self.inscripcion_evento_FK.id)+' '+ self.es_ganador

#Tabla Pago

tipos_pago = (
	('jugador','Jugador'),
	('streamer','Streamer'),
	)

class Pago(models.Model):
	tipo_pago               =models.CharField(max_length=200, choices=tipos_pago)
	fecha_hora_pago         =models.DateTimeField()
	foto                    =models.ImageField()
	valor_pago              =models.IntegerField()
	estado_pago             =models.IntegerField()
	# pago_equipo
	id_evento_FK   =models.ForeignKey(Evento, on_delete=models.PROTECT)
	
	def __str__ (self):
		return str(self.id)

#Tabla Fraude

class Reportes(models.Model):	
	fecha_hora          =models.DateTimeField(auto_now_add=True)    
	descripsion         =models.CharField(max_length=200)
	asunto              =models.CharField(max_length=200)
	Reporte_evento_FK    =models.ForeignKey(Evento, on_delete=models.PROTECT)
	
	def __str__ (self):
		return self.tipo_fraude                                                                                                                             
