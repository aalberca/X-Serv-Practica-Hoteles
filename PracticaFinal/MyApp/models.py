from django.db import models

# Create your models here.
class Alojamiento(models.Model):
    #hay que pmirar los campos del XML
    categoria = models.CharField(max_length=32)
    subcategoria = models.CharField(max_length=32) #va a poner directamente 4escrellas, o 1estrella
    nombre = models.CharField(max_length=32)
    descripcion = models.TextField()
    web = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    cod_postal = models.IntegerField()
    visitas = models.IntegerField(default=0)

    # si una imagen fuera de varios hoteles tambien seria necesario pponer el ForeignKey en HOTEL , pero como aqui una imagen es solo de un hotel se pone el ForeignKeyen la tabla imagenes
class Imagenes(models.Model):
    hotel = models.ForeignKey(Alojamiento)
    url = models.CharField(max_length=132)

class Comentarios(models.Model):
    hotel = models.ForeignKey(Alojamiento)
    texto = models.TextField()
    usuario = models.CharField(max_length=32)
    fecha = models.DateField(auto_now = True)

class Seleccionados(models.Model):
    hotel = models.ForeignKey(Alojamiento)
    usuario = models.CharField(max_length=32)
    fecha = models.DateField(auto_now = True)

class Modificaciones(models.Model):
    usuario = models.CharField(max_length=32)
    titulo = models.CharField(max_length=64, default='')
    letra = models.CharField(max_length=32)
    color = models.CharField(max_length=32)

class Likes(models.Model):
    hotel = models.ForeignKey(Alojamiento)
    usuario = models.CharField(max_length=100)
