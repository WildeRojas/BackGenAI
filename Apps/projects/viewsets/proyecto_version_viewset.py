from rest_framework import viewsets, permissions
from Apps.projects.models.proyecto_version import ProyectoVersion
from Apps.projects.models.proyecto import Proyecto
from drf_spectacular.utils import extend_schema, extend_schema_view
from Apps.projects.serializers.proyecto_version_serializer import ProyectoVersionSerializer



@extend_schema_view(
    list=extend_schema(tags=["Proyecto-Version"]),
    retrieve=extend_schema(tags=["Proyecto-Version"]),
    create=extend_schema(tags=["Proyecto-Version"]),
    update=extend_schema(tags=["Proyecto-Version"]),
    partial_update=extend_schema(tags=["Proyecto-Version"]),
    destroy=extend_schema(tags=["Proyecto-Version"]),
)


class ProyectoVersionViewSet(viewsets.ModelViewSet):
    queryset = ProyectoVersion.objects.all()
    serializer_class = ProyectoVersionSerializer
    
    def perform_create(self, serializer):
        proyecto_id = self.request.data.get("Proyecto")
        proyecto = Proyecto.objects.get(id=proyecto_id)
        ultima_version = ProyectoVersion.objects.filter(Proyecto=proyecto).order_by('-Fecha_Creacion').first()
        numero_version = int(ultima_version.Version) + 1 if ultima_version else 1
        serializer.save(Proyecto=proyecto, Version=str(numero_version))