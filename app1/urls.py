from django.urls import path
from . import views

urlpatterns = [
    path('importacion/', views.importacion, name='importacion'),
    path('borrar_todo/', views.borrar_todo, name='borrar_todo'),
]
