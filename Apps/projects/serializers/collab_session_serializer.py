from rest_framework import serializers
from Apps.projects.models.collab_session import CollabSession
from Apps.authentication.models import User
from Apps.projects.serializers.member_session_serializer import MemberSessionSerializer
from Apps.authentication.serializers.users_serializer import UserSerializer
        
class CollabSessionSerializer(serializers.ModelSerializer):
    host_user = UserSerializer(read_only = True)
    host_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='host_user', 
        write_only=True
    )
    members = MemberSessionSerializer(many=True, read_only=True)
    
    class Meta: 
        model = CollabSession
        fields = [
            'id', 'room_id', 'session_name', 'description', 'status',
            'max_participants', 'is_public', 'created_at', 'updated_at', 'ended_at',
            'invitation_code', 'host_user', 'host_user_id',
            'members'
        ]
        read_only_fields = ['id', 'room_id', 'invitation_code', 'created_at', 'updated_at', 'ended_at']