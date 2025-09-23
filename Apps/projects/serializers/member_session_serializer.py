from rest_framework import serializers
from Apps.projects.models.member_session import MemberSession
from Apps.authentication.serializers.users_serializer import UserSerializer
from Apps.authentication.models import User

class MemberSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(
        source = "user.id",
        write_only=True,
        required=False,
        allow_null=True
    )
    
    def validate(self, data):
        user = data.get("user", None)
        anonymous_name = data.get("anonymous_name", None)
        if not user and not anonymous_name:
            raise serializers.ValidationError("Debe proporcionar un usuario registrado o un nombre anónimo.")
        
        
        return data
    
    class Meta: 
        model = MemberSession
        fields = [
            'id', 'session', 'user', 'user_id', 'anonymous_name',
            'anonymous_color', 'is_active', 'is_online',
            'cursor_position', 'channel_name',
            'joined_at', 'last_activity', 'left_at'
        ]
        read_only_fields = ['id', 'joined_at', 'last_activity', 'left_at']
        