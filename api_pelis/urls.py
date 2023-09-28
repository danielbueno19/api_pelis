from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

routers = routers.DefaultRouter()

routers.register('peliculas', views.PeliculaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(routers.urls)),
    path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/favorita/', views.MarcarPeliculaFavorita.as_view()),
    path('api/v1/favoritas/', views.ListarPeliculasFavoritas.as_view()),
]

'''
1) la primera ruta que se establece es la de la app api
 - include: nos permite incluir u conjunto de vistas a diferencia de path que es solo una a la vez
 - routers: crea las rutas de manera automatica
2) configuracion de url de la autenticacion por token (auth)
3) configuración de url para /FAVORITA/
'''