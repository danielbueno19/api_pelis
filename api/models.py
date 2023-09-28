from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete

class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    estreno = models.IntegerField(default=2000)
    imagen = models.URLField(help_text='De imdb mismo')
    resumen = models.TextField(help_text='Descripcion corta')
    favoritos = models.IntegerField(default=0)

    class Meta:
        ordering = ['titulo']

class PeliculaFavorita(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

def update_favoritos(sender, instance, **kwargs):
    count = instance.pelicula.peliculafavorita_set.all().count()
    instance.pelicula.favoritos = count
    instance.pelicula.save()

# en el post delete se pasa la copia de la instance que ya no existe
post_save.connect(update_favoritos, sender=PeliculaFavorita)
post_delete.connect(update_favoritos, sender=PeliculaFavorita)


'''
1) empezaremos por crear el serializador
2) crearemos los modelos que van a relacionar las peliculas con usuarios
 - importamos User: libreria interna 
 - y vamos al serializado , para serializar esta nueva clase
3) vamos a crear una clase capaz de listas las peliculas con mas me gusta
 - para lo cual vamos a modificar la clase Pelicula, para hacer uso de filtros (con una personalizacion en el)
 - agregamos entonces el campo FAVORITOS donde almacena el nuemero de favoritos que tiene la PELI
 - existe algo dentro de DRF que son las señases, que son tipo: before edit, after save....
 - importamos post_save, post_delete para generar una accion despues de que se guarda o despus de que se elimina
 - sender: hace referencia al modelo que va a estar ejecutando la señal
 - instance: la instancia antes de que se guarde y antes de que se borre
 - Configuramos las 2 señales

'''