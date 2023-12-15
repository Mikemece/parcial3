from django.urls import path
from parcial3_beapp import views

urlpatterns = [

    path('api/eventos/<str:idp>/', views.evento),
    path('api/eventos/', views.eventos),
    path('api/eventoPostal/<str:postal>/', views.eventoPostal),
    path('api/image/upload', views.upload_image),
    path('logged', views.oauth)

]