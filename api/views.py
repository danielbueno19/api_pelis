from rest_framework import viewsets, views, filters

from .models import Pelicula, PeliculaFavorita
from .serializers import PeliculaSerializer, PeliculaFavoritaSerializer

from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer

    #Filtros
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo']
    ordering_fields = ['favoritos']


class MarcarPeliculaFavorita(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        pelicula = get_object_or_404(
            Pelicula, id= self.request.data.get('id',0)
        )

        favorita, created = PeliculaFavorita.objects.get_or_create(
            pelicula = pelicula, usuario = request.user
        )
        # En principo se asume que se crea OK
        content = {
            'id': pelicula.id,
            'favorita': True
        }
        # Si no se crea quiere decir que ya existe, entonces lo borramos
        if not created:
            favorita.delete()
            content['favorita'] = False

        return Response(content)

class ListarPeliculasFavoritas(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET para hacer lecturas
    def get (self, request):
        # Obtenemos las películas de la base de datos
        peliculas_favoritas = PeliculaFavorita.objects.filter(usuario= request.user)
        serializer = PeliculaFavoritaSerializer(peliculas_favoritas, many = True)

        return Response(serializer.data)


'''
1) se creara las vistas para manipular las peliculas
 - queryset: consulta base que se va a ajecutar cuando se quiera ver el contenido del conjunto de vistas (listarlas) y en la siguiente linea se serializa a formato JSON
 - queda establecer la ruta en el archivo urls.py de la carpeta raiz
2) crearemos la clase MarcarPeliculaFavorita, la cual validara que este autenticado a demas de que lo este mediante token valido
 - redefinimos el metodo PUT donde estaremos recuperando REQUEST que trae informacion de la peticion y del usuario que esta identidicado (TokenAuthentication)
 - vamos a buscar una pelicula a partir del identificador de pasemos como argumento
 - crearemos la instancia de la pelicula favorita, ese relacion entre usuario y la pelicula que selecciono como favorita (get_or_create) tratara de encontar una instancia de favorita, en caso de no existir la creara returnado True o False en caso de no poder craerla.
 - crearemos un diccionario con el formaro JSON (content) de respuesta
 - queda conectar esta nueva clase a una url
3) creamos la clase ListarPeliculasFavoritas, la cual se encargara de listar las peliculas favoritas seleccionadas por un usuario
 - creamos su respectiva ruta en las url
4) Añadiremos a la clase PeliculaViewSet los filtros, para lo cual importamos filters
 - search_fields: estblece por cual dato se va a hacer la busqueda
 - ordering_fields: define cual va a ser el criterio por el cual se va a ordenar
'''