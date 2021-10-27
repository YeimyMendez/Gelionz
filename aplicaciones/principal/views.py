from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from . forms import *
from django.contrib import messages
from django.core.mail import EmailMessage, message
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

#VISTAS DE USUARIO ANONIMO
#VISTA DE CONTACTO
def contacto(request):
	formulario_contacto=FormularioContacto()
	if request.method=="POST":
		formulario_contacto=FormularioContacto(data=request.POST)
		if formulario_contacto.is_valid():
			nombre=request.POST.get("nombre")
			email=request.POST.get("email")
			contenido=request.POST.get("contenido")
			email=EmailMessage("Mensaje desde app Gelionz", "El usuario con nombre {} con la direccion {} escribe lo siguiente: \n\n {}".format(nombre,email,contenido),"",["gelionzgamer@gmail.com"],reply_to=[email])
			try:
				email.send()
				return redirect("/contacto/?valido")
			except:
				return redirect("/contacto/?novalido")
	return render(request, "contacto.html", {'miFormulario':formulario_contacto})
	
#Vista home
def home(request):
	print(request.user.username)
	return render(request, "home.html")

def blog(request):

    blogs=Evento.objects.all()
    return render(request, 'blog.html', locals())

#vista register
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('login')
	else:
		form = UserRegisterForm()
		context = { 'form' : form }
	return render(request, 'register.html', locals())

#Vista de Login reescrito del login por defecto
@login_required
def post(request):
	current_user = get_object_or_404(Usuario, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Post enviado')
			return redirect('perfil')
	else:
		form = PostForm()
	return render(request, '', {'form' : form })

#Vista de perfil (seleccion de rol)
def perfil(request, username=None):
	try:
		#current_user = request.user
		user = Usuario.objects.get(username=request.user.username)
	except:
		pass
	if user.rol_de_usuario == 'jugador':
		return render(request, 'perfil.html', locals()) 
	elif user.rol_de_usuario == 'streaming':
		return render(request, 'inicio_streaming.html', locals()) 
	else:
		return redirect('home')

@login_required
def imgPerfil(request):
	if request.method == 'POST':
		print("xxxxxxxxxx")
		print()
		print("xxxxxxxxxx")
		form = ImgPerfilForm(request.POST, request.FILES)
		
		if form.is_valid():
			form.save()
			messages.success(request, f'Image uploaded succesfully!')
			# message = "Image uploaded succesfully!"
		else:
			form = ImgPerfilForm()

	return render(request,'perfil.html', locals())







	# usuario = request.user.id
	# cambiar_img  = Usuario.objects.get(user__id=usuario)
	# # edit_imagen  = Usuario.objects.get(id=usuario)

	# if request.method == 'POST':
	# 	form = ImgPerfilForm(request.POST, request.FILES, instance = cambiar_img)
	# 	if form.is_valid():
	# 		cambiar_img=form.cleaned_data.get('imagen')
	# 		cambiar_img.save()#,perfil=User.username

	# 		return redirect('perfil.html',username=request.usuario.username)
	# else:
	# 	form = ImgPerfilForm(instance=cambiar_img)
		
	# context={
	# 	'form':form,
	# }

	# return render(request,'perfil.html', context)

#VISTAS DE USUARIO STREAMER
def inicio_view(request):
	persona = Usuario.objects.get(username=request.user.username)
	lista = Evento.objects.filter(organizador = persona)
	return render(request, 'inicio_streaming.html', locals())

#VISTA DE LISTA DE EVENTOS (TORNEOS O PARTIDAS)
def listar_evento_view(request, vista):
	try:
		persona = Usuario.objects.get(username=request.user.username)
		lista = Evento.objects.filter(tipo_evento = vista , organizador = persona)
	except:
		pass
	return render(request, 'listar_evento.html', locals())

#VISTA DE AGREGAR EVENTO (TORNEOS O PARTIDAS)
@login_required
def agregar_evento_view(request):
	perfil = Usuario.objects.get(username=request.user.username)
	if request.method == 'POST':
		formulario = form_agregar_evento(request.POST, request.FILES)
		if formulario.is_valid():
			f=formulario.save(commit=False)
			f.organizador = perfil
			f.save()
			messages.success(request, f'El evento fue creado Exitosamente')
			return redirect ('/principal/listar_evento/{}/'.format(f.tipo_evento))
	else: #GET
		formulario = form_agregar_evento()
	return render(request, 'agregar_evento.html', locals())

#VISTA DE DETALLES (TORNEOS O PARTIDAS)
def detalle_view(request, id_evento):
	obj = Evento.objects.get(id=id_evento)
	lista =  Inscripcion.objects.filter(inscripcion_evento_FK__id=id_evento)
	return render(request, 'detalle.html', locals())

#VISTA DE EDITAR (TORNEOS O PARTIDAS)
def editarE_view(request, id_evento):
	objeto = Evento.objects.get(id=id_evento)
	if request.method == 'POST':
		formulario  = form_agregar_evento(request.POST, request.FILES, instance = objeto)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			f.save()
			return redirect ('/principal/listar_evento/{}/'.format(f.tipo_evento))
	else:
		formulario = form_agregar_evento(instance = objeto)
	return render (request, 'agregar_evento.html', locals())

#VISTA DE AGRGAR eL JUGADOR GANADOR DE (TORNEOS O PARTIDAS)
def agregarG_view(request, id_evento, id_equipo):
	equipo_inscrito = Inscripcion.objects.get(inscripcion_evento_FK__id=id_evento, id_equipo_FK__id=id_equipo)
	equipo_inscrito.es_ganador='ganador'
	equipo_inscrito.save()
	obj_evento = Evento.objects.get(id=id_evento)
	obj_equipo = Equipo.objects.get(id=id_equipo)
	obj_evento.ganador_evento=obj_equipo.nombre_equipo
	obj_evento.save()
	objeto = Evento.objects.get(id=id_evento)
	#cambiamos el estado de inscritos a perdedores al resto de equipostos
	# Si uiere cambiar el estado  a todos los inscritos por perdedr se puede hacer  pero te toca cambiar el estado de cada uno  usando un CIBLO WHILE O FOR
	
	inscritos = Inscripcion.objects.filter(inscripcion_evento_FK__id=id_evento)
	for x in inscritos:
		if x != equipo_inscrito: #que lo haga si es diferente al ganador 
			x.es_ganador = 'perdedor'
	# Probar a ver como le va con este bloque 
	
	return redirect('/principal/detalle/{}/'.format(obj_evento.id))

#VISTA DE ELIMINAR (TORNEOS O PARTIDAS)
def eliminarEvento_view(request, id_evento):
	try:
		objeto = Evento.objects.get(id=id_evento)
		objeto.delete()
	except:
		pass
	return redirect ('/principal/inicio/')

#VISTA DE PAGOS REALIZADIOS ALUSUARIO STREAMER DE PARTIDAS O TORNEOS
def pagos_view(request):
	perfil = Usuario.objects.get(username=request.user.username)
	lista  = Pago.objects.filter()
	return render(request, 'pagos.html', locals())



#VISTAS DE USUARIO JUGADOR
def lista_equipos(request):
	try:
		persona = Usuario.objects.get(username=request.user.username)
		#lista_equipos = Equipo.objects.filter(nombre_capitan=persona.username)
		lista_equipos = User_Equipo.objects.filter(user=persona)
	except:
		pass
	return render(request, 'lista_equipos.html', locals())


#VISTA DE CREAR EQUIPOS
def crear_equipo(request):
	persona = Usuario.objects.get(username=request.user.username)
	if request.method == 'POST':
		formulario = form_crear_equipo(request.POST, request.FILES)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			f.nombre_capitan = persona.username
			f.save()
			mi_equipo = User_Equipo()
			mi_equipo.equipo_FK= f
			mi_equipo.user = persona
			mi_equipo.save()
			messages.success(request, f'El equipo {f} fue creado Exitosamente')
			return redirect ('/principal/lista_equipos/')
	else: #GET
		formulario = form_crear_equipo()
	return render(request, 'crear_equipo.html', locals())

#VISTA DE DETALLES EQUIPOS
def detalle_equipo(request, id_equipo):
	obj = Equipo.objects.get(id=id_equipo)
	busqueda = request.POST.get("buscar")
	#jugadores = Usuario.objects.all()

	if busqueda:
		jugadores = Usuario.objects.filter(
			Q(username__icontains = busqueda) |
			Q(nombres__icontains = busqueda) |           
			Q(apellidos__icontains = busqueda) |
			Q(email__icontains = busqueda)    
		).distinct()

	asociados = User_Equipo.objects.filter(equipo_FK = obj)
	
	return render(request, 'detalle_equipo.html', locals())

def asociar_equipo (request, id_equipo, id_jugador):
	equipo = Equipo.objects.get(id=id_equipo) # remplazar por evento
	jugador = Usuario.objects.get(id = id_jugador) # remplazar por eequipo
	try:
		# buscar si el usuairo ya esta asociado al equipo
		team =  User_Equipo.objects.filter(equipo_FK = equipo, user = jugador)
		if team:
			messages.error(request, f'YA ESTA INSCRITO {jugador} EN EL EQUIPO')
			
		else:
			asociados = User_Equipo()
			## no dejar asociar a alguien asociado al equipo
			# para no agregar al equipo 2 veces 	
			asociados.equipo_FK = equipo
			asociados.user = jugador
			asociados.save()
			messages.success(request, f'SE ASOCIO AL {equipo}')
	except:
		pass
	return redirect('/principal/detalle_equipo/{}/'.format(equipo.id))

#VISTA DE DETALLES MIENBRO DE EQUIPO BUSCADOR
def listar_jugador(request):
	busqueda = request.POST.get("buscar")
	jugadores = Usuario.objects.all()
	if request.method.POST:
		print("xxxxxxxxxx")
		print(busqueda)
		print("xxxxxxxxxx")

	if busqueda:
		jugadores = Usuario.objects.filter(
			Q(username__icontains = busqueda) |
			Q(nombres__icontains = busqueda) |           
			Q(apellidos__icontains = busqueda) |
			Q(email__icontains = busqueda)    
		).distinct()
	ctx = {'jugadores':jugadores}
	return render(request, 'detalle_equipo.html', ctx )

#Vista Nivel Competitivo
def NivelCompetitivo(request):
	levento=Evento.objects.all()
	return render(request, 'nivel_competitivo.html', locals())
#vista Inscribirme
def inscribirEquipo (request,  id_evento, id_equipo):
	evento_objeto = Evento.objects.get(id=id_evento)
	equipo_objeto = User_Equipo.objects.get(id = id_equipo)
	
	try:
		# buscar si el usuairo ya esta asociado al equipo
		team =  Inscripcion.objects.filter(inscripcion_evento_FK = evento_objeto, id_equipo_FK = equipo_objeto.equipo_FK)
		if team:
			messages.error(request, f'EL EQUIPO {equipo_objeto.equipo_FK} YA SE ENCUENTRA INSCRITO AL EVENTO')			
		else:
			asociados = Inscripcion()
			## no dejar asociar a alguien asociado al equipo
			# para no agregar al equipo 2 veces 	
			asociados.inscripcion_evento_FK = evento_objeto
			asociados.id_equipo_FK = equipo_objeto.equipo_FK
			asociados.save()
			messages.success(request, f'EL EQUIPO {equipo_objeto} SE INSCRIBIO EXITOSAMENTE')	
	except:
		pass
	#return redirect('/principal/inscribirEvento/{}/'.format(evento_objeto.id))
	return redirect('lista_equipos')

def seleccionar_equipo(request, id_evento):
	levento=Evento.objects.filter()
	mis_equipos = User_Equipo.objects.filter(user = request.user)

	return render(request, 'seleccionar_equipo.html', locals())


