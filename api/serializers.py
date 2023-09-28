from rest_framework import serializers
from .models import Pelicula, PeliculaFavorita

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'

class PeliculaFavoritaSerializer(serializers.ModelSerializer):
    pelicula = PeliculaSerializer()
    class Meta:
        model=PeliculaFavorita
        fields = ['pelicula']

'''
1) es la clase que se encargara de generar una respuesta JSON de los campos establecidos, en este todos __all__
2) creamos el serializador de la nueva clase PeliculaFavorita
'''