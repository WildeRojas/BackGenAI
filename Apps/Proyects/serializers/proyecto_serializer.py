from rest_framework import serializers
from Apps.Proyects.models.proyecto import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'