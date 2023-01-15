from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('/<int:element>', views.home, name="home_cuota"),
    path('create/', views.create, name="create"),
    path('cuotaPagar/', views.cuotaPagar, name="cuotaPagar"),
    path('cuotaEliminar/', views.cuotaEliminar, name="cuotaEliminar"),
    path('actualizarFecha/', views.actualizarFecha, name="actualizarFecha")
]