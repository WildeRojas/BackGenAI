from rest_framework import viewsets
from Apps.Proyects.models.proyecto import Proyecto
from Apps.Proyects.serializers.proyecto_serializer import ProyectoSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Proyectos'])
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer