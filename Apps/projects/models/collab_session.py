import secrets
import uuid
from django.db import models
from Apps.authentication.models import User
from django.conf import settings

class CollabSession(models.Model):
    SESSION_STATUS = [
        ('active', 'Activa'),
        ('ended', 'Finalizada'),
    ]
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    host_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_sessions')
    session_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=SESSION_STATUS, default='active')
    max_participants = models.PositiveIntegerField(default=10)
    is_public = models.BooleanField(default=True)  # Por defecto es pública
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    invitation_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sesión de Colaboración'
        verbose_name_plural = 'Sesiones de Colaboración'
    
    def __str__(self):
        return f"{self.session_name}"
    
    def save(self, *args, **kwargs):
        # Generar código de invitación si no existe
        if not self.invitation_code:
            self.invitation_code = secrets.token_urlsafe(8)
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        """Verifica si la sesión está activa"""
        return self.status == 'active'
    
    @property
    def participants_count(self):
        """Cuenta el número de participantes activos"""
        return self.members.filter(is_active=True).count()
    
    @property
    def can_join(self):
        """Verifica si se pueden unir más participantes"""
        return self.is_active and self.participants_count < self.max_participants
    
    def get_invitation_link(self):
        """Genera el link de invitación para la sesión"""
        base_url = getattr(settings, "FRONTEND_BASE_URL", "http://localhost:5173")
        return f"{base_url}/collaborate/{self.room_id}?code={self.invitation_code}"
    
    def end_session(self):
        """Finaliza la sesión y desactiva todos los miembros"""
        from django.utils import timezone
        
        self.status = 'ended'
        self.ended_at = timezone.now()
        self.save()
        
        # Desactivar todos los miembros
        self.members.update(is_active=False)
