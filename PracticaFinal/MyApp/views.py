
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import Alojamiento, Imagenes, Comentarios, Seleccionados, Modificaciones, Likes
from MyApp.parsea import parsear_fichero
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User


# Create your views here.

def cargar_bd(request, idioma, identificador): # este procedimiento guarda los datos del xml en la base de datos
                            # antes comprueba que el idioma es el espanol, pues en caso contrario no se guardan

    if idioma == "english":
        datos = parsear_fichero('http://www.esmadrid.com/opendata/alojamientos_v1_en.xml')
    elif idioma == "french":
        datos = parsear_fichero('http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml')
    else:
        datos = parsear_fichero('http://www.esmadrid.com/opendata/alojamientos_v1_es.xml')

    for hotel in datos: # hotel es un diccionario, porque datos es una lista de diccionarios
        nombre = hotel.get('name')
        #print hotel
        if hotel.has_key('body'):
            descripcion = hotel.get('body')
        else:
            descripcion = ''
        web = hotel.get('web')
        telefono = hotel.get('phone')
        direccion = hotel.get('address')
        cod_postal = hotel.get('zipcode')
        categoria = hotel.get('Categoria')
        if hotel.has_key('SubCategoria'):
            subcategoria = hotel.get('SubCategoria')
        else:
            subcategoria = '0 estrellas'

        if idioma == 'spanish':
            nuevo_aloj = Alojamiento(categoria = categoria, subcategoria = subcategoria, nombre = nombre, descripcion = descripcion, web = web, telefono = telefono, direccion = direccion, cod_postal = cod_postal)
            nuevo_aloj.save()
            for elemento in hotel.get('url_fotos'):
                nombre_hotel = Alojamiento.objects.get(nombre = nombre)
                nueva_foto = Imagenes(hotel = nombre_hotel, url = elemento)
                nueva_foto.save()
        else:
            aloj = Alojamiento.objects.get(id=int(identificador))
            aloj_nombre = aloj.nombre
            #print aloj_nombre
            if nombre == aloj_nombre:
                return (nombre, descripcion, web, telefono, direccion, cod_postal, categoria, subcategoria)


def ordenar_maximos_comentarios():
    todos_hoteles = Alojamiento.objects.all()
    dicc_hotel_coment = {}
    for hotel in todos_hoteles:
        if hotel.comentarios_set.count() != 0:
            dicc_hotel_coment[hotel.nombre] = hotel.comentarios_set.count() # supuestamente cuenta los comentarios que hay, los guardo en un diccionario
                                                                        # donde la clave es el hotel y el valor el numero de comentarios

    if len(dicc_hotel_coment) != 0:
        list_hotel_coment = dicc_hotel_coment.items() #lo tengo que pasar a lista para poder ordenarlo
        list_hotel_coment.sort(key=lambda x: x[1], reverse=True)

        if len(list_hotel_coment) >= 10:
            list_hotel_coment = list_hotel_coment[:10]
    else:
        list_hotel_coment = []

    return list_hotel_coment

def pag_principal(request):
    if request.method == 'GET':
        if Alojamiento.objects.count() == 0:
            template = get_template('primera_vez.html')
            context = RequestContext(request)
        else:
            try:
                lista_usuarios = User.objects.all()
                lista_titulos = []
                for usu in lista_usuarios:
                    try:
                        mod = Modificaciones.objects.get(usuario=usu.username)
                        if mod.titulo != '':
                            titulo = mod.titulo
                        else:
                            titulo = "Pagina de " + usu.username
                        lista_titulos.append((titulo, usu.username))
                    except:
                        titulo = "Pagina de " + usu.username
                        lista_titulos.append((titulo, usu.username))
            except:
                lista_usuarios = []
            lista_nombres_hoteles = ordenar_maximos_comentarios()
            if len(lista_nombres_hoteles) == 0:
                vacio = True
            else:
                vacio = False
            lista_hoteles = []
            for nombre in lista_nombres_hoteles:
                hotel = Alojamiento.objects.get(nombre = nombre[0])
                try:
                    fotos = Imagenes.objects.filter(hotel = hotel)
                except ObjectDoesNotExist:
                    fotos = []
                if len(fotos) == 0:
                    buena = ''
                for foto in fotos:
                    buena = foto.url
                lista_hoteles.append((hotel, buena))
            template = get_template('pag_ppal.html')
            context = RequestContext(request, {'lista_hoteles': lista_hoteles, 'lista_titulos': lista_titulos, 'vacio': vacio})
        return HttpResponse(template.render(context))

def cargar_datos(request):
    if request.method == 'GET':
        cargar_bd(request, "spanish", 0) #considero que esos son valores por defecto, pues estoy segura de que llamano al procedimiento por aqui es en espanol y no necesito ninguno de os 3 parametros
        try:
            lista_usuarios = User.objects.all()
        except:
            lista_usuarios = []
        lista_hoteles = ordenar_maximos_comentarios()
        return HttpResponseRedirect("/")

def pag_usuario(request, usuario):
    try:
        modificacion = Modificaciones.objects.get(usuario=usuario)
        titulo = modificacion.titulo
    except:
        titulo = ''
    sus_alojamientos = Seleccionados.objects.filter(usuario = usuario)
    lista_hoteles = []
    for aloj in sus_alojamientos:
        fecha = aloj.fecha
        hotel = Alojamiento.objects.get(nombre = aloj.hotel.nombre)
        try:
            fotos = Imagenes.objects.filter(hotel = hotel)
        except ObjectDoesNotExist:
            fotos = []
        if len(fotos) == 0:
            buena = ''
        for foto in fotos:
            buena = foto.url
        lista_hoteles.append((hotel, buena, fecha))

    if len(lista_hoteles) == 0:
        vacio = True
    else:
        vacio = False

    template = get_template('pag_usuario.html')
    context = RequestContext(request, {'lista_hoteles': lista_hoteles, 'vacio': vacio, 'titulo': titulo, 'usuario':usuario})
    return HttpResponse(template.render(context))


@csrf_exempt
def pag_todos_aloj(request):
    if request.method == 'GET':
        alojamientos = Alojamiento.objects.all()

    elif request.method == 'POST':
        categoria = request.body.split('&')[1].split('=')[1]
        categoria = poner_espacios(categoria)[:-1]
        subcategoria = request.body.split('&')[2].split('=')[1]
        subcategoria = poner_espacios(subcategoria)[:-1]

        if categoria != "Todos" and subcategoria != "Todos":
            alojamientos = Alojamiento.objects.filter(categoria = categoria, subcategoria=subcategoria)
        elif categoria == "Todos" and subcategoria != "Todos":
            alojamientos = Alojamiento.objects.filter(subcategoria = subcategoria)
        elif categoria != "Todos" and subcategoria == "Todos":
            alojamientos = Alojamiento.objects.filter(categoria = categoria)
        elif categoria == "Todos" and subcategoria == "Todos":
            alojamientos = Alojamiento.objects.all()

    lista_aloj=[]
    for aloj in alojamientos:
        lista_aloj.append((aloj.nombre, aloj.id))

    template = get_template('muestra_alojamientos.html')
    context = RequestContext(request, {'lista_aloj': lista_aloj})
    return HttpResponse(template.render(context))

def pag_aloj(request, identificador):
    alojamiento = Alojamiento.objects.get(id = int(identificador))
    nombre = alojamiento.nombre
    fotos = Imagenes.objects.filter(hotel = alojamiento)
    if len(fotos) > 5:
        fotos = fotos[:5]
    lista_fotos=[]
    for foto in fotos:
        lista_fotos.append(foto.url)
        print foto.url
    comentarios = Comentarios.objects.filter(hotel = alojamiento)
    if len(comentarios) != 0:
        Comentarios_vacio = False;
    else:
        Comentarios_vacio = True;
    try:
        coment_usu = Comentarios.objects.get(hotel = alojamiento, usuario = request.user.username)
        NoComent = False
    except ObjectDoesNotExist:
        NoComent = True
    lista_comentarios=[]
    for coment in comentarios:
        lista_comentarios.append((coment.usuario, coment.texto, coment.fecha))

    visitas = contador_visitas(identificador)
    megustas = contador_megustas(identificador)
    template = get_template('pag_alojamiento.html')
    context = RequestContext(request, {'alojamiento': alojamiento,'comentarios': lista_comentarios, 'fotos': lista_fotos, 'NoComent': NoComent, 'Comentarios_vacio': Comentarios_vacio, 'visitas': visitas, 'megustas': megustas})
    return HttpResponse(template.render(context))

def about(request):
    template = get_template('about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def crear_xml(request, usuario):
    sus_alojamientos = Seleccionados.objects.filter(usuario = usuario)
    lista_todo = []
    for aloja in sus_alojamientos:
        sus_fotos = Imagenes.objects.filter(hotel=aloja.hotel)
        lista_fotos=[]
        for foto in sus_fotos:
            lista_fotos.append(foto.url) #estas son las fotos de un alojamiento
        lista_todo.append((aloja, lista_fotos)) #esta es una lista de listas, que tiene toooodas las fotos
    template = get_template('fichero_xml.xml')
    context = RequestContext(request, {'lista_todo': lista_todo})
    return HttpResponse(template.render(context), content_type="text/xml")

@csrf_exempt
def poner_comentario(request, identificador):
    if request.method == 'POST':
        usuario = request.user.username
        aloj = Alojamiento.objects.get(id=int(identificador))
        comentario = request.body.split('&')[0].split('=')[1] #el primer 1 depende de lo que imprima el request.body pq a veces el primer campo es algo que pone el navegador
        comentario = poner_espacios(comentario)
        nuevo_comentario = Comentarios(hotel=aloj, texto=comentario, usuario=usuario)
        nuevo_comentario.save()
        direccion = "/alojamientos/" + str(identificador)
        return HttpResponseRedirect(direccion)
    else:
        return HttpResponse("ERROOOOOOR")

def poner_espacios(frase_inicial):
    palabras = frase_inicial.split('+')
    frase = ''
    for palabra in palabras:

        frase += palabra + ' '
    return frase

def pag_aloj_otro_idioma(request, idioma, identificador):
    try:
        (nombre, descripcion, web, telefono, direccion, cod_postal, categoria, subcategoria) = cargar_bd(request, idioma, identificador)
    except:
        template = get_template('error.html')
        return HttpResponse(template.render(Context({'texto': "Lo sentimos, este alojamiento no esta disponible en dicho idioma"})))

    alojamiento = Alojamiento.objects.get(nombre=nombre)
    fotos = Imagenes.objects.filter(hotel = alojamiento)
    if len(fotos) > 5:
        fotos = fotos[:5]
    lista_fotos=[]
    for foto in fotos:
        lista_fotos.append(foto.url)
    comentarios = Comentarios.objects.filter(hotel = alojamiento)
    if len(comentarios) != 0:
        Comentarios_vacio = False;
    else:
        Comentarios_vacio = True;
    coment_usu = Comentarios.objects.filter(usuario = request.user.username)
    if coment_usu != None:
        NoComent = False
    else:
        NoComent = True
    lista_comentarios=[]
    for coment in comentarios:
        lista_comentarios.append((coment.usuario, coment.texto, coment.fecha))

    visitas = contador_visitas(identificador)
    megustas = contador_megustas(identificador)

    if idioma == "english":
        template = get_template('pag_alojamiento_ingles.html')
    elif idioma == "french":
        template = get_template('pag_alojamiento_frances.html')
    context = RequestContext(request, {'id': identificador, 'nombre': nombre, 'descripcion': descripcion, 'web': web,
                                        'direccion': direccion, 'cod_postal': cod_postal,
                                        'telefono': telefono, 'subcategoria': subcategoria,
                                        'comentarios': lista_comentarios, 'fotos': lista_fotos, 'NoComent': NoComent,
                                        'Comentarios_vacio': Comentarios_vacio, 'visitas': visitas, 'megustas': megustas})
    return HttpResponse(template.render(context))


@csrf_exempt
def login(request):

    username = request.body.split('&')[1].split('=')[1]
    password = request.body.split('&')[2].split('=')[1]

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect('/')
    else:
        template = get_template('error.html')
        return HttpResponse(template.render(Context({'texto': "Usuario no autenticado"})))

def anadir_hotel_pag(request, identificador):
    try:
        aloj = Alojamiento.objects.get(id=int(identificador))
    except ObjectDoesNotExist:
        template = get_template('error.html')
        return HttpResponse(template.render(Context({'texto': "Lo sentimos, no existe alojamiento con dicho identificador"})))
    usuario = request.user.username
    hotel_anadido = Seleccionados(hotel=aloj, usuario=usuario)
    hotel_anadido.save()

    direccion = '/' + usuario
    return HttpResponseRedirect(direccion)


def css(request):
    usuario = request.user.username
    letra_defecto = '1.3em'
    color_defecto = 'white'
    titulo_defecto = "Pagina de " + request.user.username

    if request.method == "POST":

        color = request.body.split('&')[1].split('=')[1]
        letra = request.body.split('&')[2].split('=')[1]

        if color != "PorDefecto" and letra != "PorDefecto":

            try:
                cambio = Modificaciones.objects.get(usuario=usuario)
                cambio.color = color
                cambio.letra = letra
                cambio.save()
            except:
                cambio = Modificaciones(usuario=usuario, titulo=titulo_defecto, letra=letra, color=color)
                cambio.save()
        elif color != "PorDefecto" and letra == "PorDefecto":
            try:
                cambio = Modificaciones.objects.get(usuario=usuario)
                cambio.color = color
                cambio.letra = letra_defecto
                cambio.save()
            except:
                cambio = Modificaciones(usuario=usuario, titulo=titulo_defecto, letra=letra_defecto, color=color)
                cambio.save()
        elif color == "PorDefecto" and letra != "PorDefecto":
            try:
                cambio = Modificaciones.objects.get(usuario=usuario)
                cambio.color = color_defecto
                cambio.letra = letra
                cambio.save()
            except:
                cambio = Modificaciones(usuario=usuario, titulo=titulo_defecto, letra=letra, color=color_defecto)
                cambio.save()
        elif color == "PorDefecto" and letra == "PorDefecto":
            try:
                cambio = Modificaciones.objects.get(usuario=usuario)
                cambio.color = color_defecto
                cambio.letra = letra_defecto
                cambio.save()
            except:
                cambio = Modificaciones(usuario=usuario, titulo=titulo_defecto, letra=letra_defecto, color=color_defecto)
                cambio.save()

        direccion = '/' + usuario
        return HttpResponseRedirect(direccion)
    elif request.method == "GET":
        color = "yellow"
        if request.user.is_authenticated:
            try:
                su_cambio = Modificaciones.objects.get(usuario=usuario)
                color = su_cambio.color
                letra = su_cambio.letra
            except:
                color = color_defecto
                letra = letra_defecto
        template = get_template('estilo_general.css')
        context = RequestContext(request, {'color': color, 'letra': letra})
        return HttpResponse(template.render(context), content_type="text/css")

def cambiar_titulo(request):
    letra_defecto = '1.3em'
    color_defecto = 'white'
    if request.method == "POST":
        titulo = request.body.split('&')[1].split('=')[1]
        titulo = poner_espacios(titulo)
        try:
            cambio = Modificaciones.objects.get(usuario=request.user.username)
            cambio.titulo = titulo
            cambio.save()
        except:
            cambio = Modificaciones(usuario=request.user.username, titulo=titulo, letra=letra_defecto, color=color_defecto)
            cambio.save()
        direccion = '/' + request.user.username
        return HttpResponseRedirect(direccion)

def contador_visitas(identificador):
    aloj = Alojamiento.objects.get(id=int(identificador))
    aloj.visitas += 1
    visitas = aloj.visitas
    aloj.save()
    return visitas

def ordenar_maximas_visitas(request):
    todos_hoteles = Alojamiento.objects.all()
    lista = []
    for hotel in todos_hoteles:
        lista.append((hotel.nombre, hotel.visitas, hotel.id))

    lista.sort(key=lambda x: x[1], reverse=True)

    template = get_template('ranking.html')
    context = RequestContext(request, {'lista':lista})
    return HttpResponse(template.render(context))

def anadir_megusta(request, identificador):
    usu_id = request.user.id
    if usu_id == None:
        usu_id = request.COOKIES['sessionid']
    aloj = Alojamiento.objects.get(id=int(identificador))
    try:
        d = Likes.objects.get(hotel=aloj, usuario=usu_id)
        #no hay que hacer nada, una misma persona no puede poner mas de un me gusta en un mismo alojamiento
    except:
        megusta = Likes(hotel=aloj, usuario=usu_id)
        megusta.save()

    direccion = '/alojamientos/' + identificador
    return HttpResponseRedirect(direccion)

def contador_megustas(identificador):
    try:
        hotel = Alojamiento.objects.get(id=int(identificador))
        lista = Likes.objects.filter(id=int(identificador))
        megustas = hotel.likes_set.count()

    except:
        megustas = 0
    return megustas

def rss(request, identificador):
    aloja = Alojamiento.objects.get(id=int(identificador))
    lista = Comentarios.objects.filter(hotel=aloja)

    template = get_template('rss_comentarios.xml')
    context = RequestContext(request, {'aloj':aloja, 'lista':lista})
    return HttpResponse(template.render(context), content_type="text/xml")

def pag_ppal_xml(request):
    lista_nombres_hoteles = ordenar_maximos_comentarios()
    if len(lista_nombres_hoteles) == 0:
        vacio = True
    else:
        vacio = False
    lista_hoteles = []
    for nombre in lista_nombres_hoteles:
        hotel = Alojamiento.objects.get(nombre = nombre[0])
        try:
            fotos = Imagenes.objects.filter(hotel = hotel)
        except ObjectDoesNotExist:
            fotos = []
        if len(fotos) == 0:
            buena = ''
        for foto in fotos:
            buena = foto.url
        lista_hoteles.append((hotel, buena))
    template = get_template('pag_ppal.xml')
    context = RequestContext(request, {'lista_hoteles': lista_hoteles, 'vacio': vacio})
    return HttpResponse(template.render(context), content_type="text/xml")
