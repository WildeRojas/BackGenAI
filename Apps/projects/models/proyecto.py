from django.db import models
from Apps.authentication.models import User

class Proyecto(models.Model):
    Titulo = models.CharField(max_length=30)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Descripcion = models.TextField()
    Fecha_Creacion = models.DateTimeField(auto_now_add=True)
    Fecha_Actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Titulo
    
    