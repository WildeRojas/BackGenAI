from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from Apps.projects.models import MemberSession
from Apps.projects.serializers.member_session_serializer import MemberSessionSerializer


@extend_schema_view(
    list=extend_schema(tags=["MemberSessions"]),
    retrieve=extend_schema(tags=["MemberSessions"]),
    create=extend_schema(tags=["MemberSessions"]),
    update=extend_schema(tags=["MemberSessions"]),
    partial_update=extend_schema(tags=["MemberSessions"]),
    destroy=extend_schema(tags=["MemberSessions"]),
)

class MemberSessionViewSet(viewsets.ModelViewSet):
    queryset = MemberSession.objects.all()
    serializer_class = MemberSessionSerializer