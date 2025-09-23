from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from Apps.projects.models import CollabSession
from Apps.projects.serializers.collab_session_serializer import CollabSessionSerializer


@extend_schema_view(
    list=extend_schema(tags=["CollabSessions"]),
    retrieve=extend_schema(tags=["CollabSessions"]),
    create=extend_schema(tags=["CollabSessions"]),
    update=extend_schema(tags=["CollabSessions"]),
    partial_update=extend_schema(tags=["CollabSessions"]),
    destroy=extend_schema(tags=["CollabSessions"]),
)
class CollabSessionViewSet(viewsets.ModelViewSet):
    queryset = CollabSession.objects.all()
    serializer_class = CollabSessionSerializer
