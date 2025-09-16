from django.urls import path, include
from rest_framework import routers
from Apps.Proyects.viewsets.proyecto_viewset import ProyectoViewSet
router = routers.DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


