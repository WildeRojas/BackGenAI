from rest_framework import serializers
from Apps.projects.models.proyecto_version import ProyectoVersion


class ProyectoVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoVersion
        fields = "__all__"
        read_only_fields = ['id', 'Fecha_Creacion', 'Fecha_Actualizacion']