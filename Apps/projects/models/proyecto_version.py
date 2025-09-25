from django.db import models
from Apps.projects.models.proyecto import Proyecto

class ProyectoVersion(models.Model):
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    Version = models.CharField(max_length=10)
    contenido = models.JSONField()
    Fecha_Creacion = models.DateTimeField(auto_now_add=True)
    Fecha_Actualizacion = models.DateTimeField(auto_now=True)

    class Meta: 
        unique_together = ('Proyecto', 'Version')
        ordering = ['-Fecha_Creacion']
    
    def __str__(self):
        return f"{self.Proyecto.Titulo} - v{self.Version}"