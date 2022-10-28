from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/delete/', views.room_delete, name='room_delete'),
    path('<slug:slug>/edit/', views.room_edit, name='room_edit')
]
