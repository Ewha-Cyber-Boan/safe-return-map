from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('findPath/', views.findPath, name = 'new_path'),
    path('markerMap/', views.markerMap, name = 'new_map')
]