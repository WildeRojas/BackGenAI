import uuid
from django.db import models
from Apps.authentication.models import User
from Apps.projects.models.collab_session import CollabSession

class MemberSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    session = models.ForeignKey(CollabSession, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_name = models.CharField(max_length=50, blank=True, null=True)
    anonymous_color = models.CharField(max_length=7, default='#2196F3')  # Color para el cursor/avatar
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)  # Si está conectado por WebSocket
    cursor_position = models.JSONField(default=dict, blank=True)  
    channel_name = models.CharField(max_length=255, blank=True, null=True)  # Para WebSocket
    joined_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['session', 'user']  # Un usuario solo puede estar una vez por sesión
        ordering = ['-joined_at']
        verbose_name = 'Miembro de Sesión'
        verbose_name_plural = 'Miembros de Sesión'
    
    def __str__(self):
        user_display = self.user.username if self.user else self.anonymous_name
        return f"{user_display} en {self.session.session_name}"
    
    @property
    def display_name(self):
        """Devuelve el nombre a mostrar (usuario registrado o anónimo)"""
        return self.user.username if self.user else self.anonymous_name or "Usuario Anónimo"
    
    @property
    def is_host(self):
        """Verifica si es el host de la sesión"""
        return self.user == self.session.host_user
    
    def update_cursor_position(self, x, y):
        """Actualiza la posición del cursor del usuario"""
        from django.utils import timezone
        
        self.cursor_position = {'x': x, 'y': y, 'timestamp': timezone.now().isoformat()}
        self.save(update_fields=['cursor_position', 'last_activity'])
    
    def go_online(self, channel_name=None):
        """Marca al usuario como conectado"""
        self.is_online = True
        if channel_name:
            self.channel_name = channel_name
        self.save(update_fields=['is_online', 'channel_name', 'last_activity'])
    
    def go_offline(self):
        """Marca al usuario como desconectado"""
        self.is_online = False
        self.channel_name = None
        self.save(update_fields=['is_online', 'channel_name'])
    
    def leave_session(self):
        """Hace que el usuario abandone la sesión"""
        from django.utils import timezone
        
        self.is_active = False
        self.is_online = False
        self.left_at = timezone.now()
        self.channel_name = None
        self.save()
