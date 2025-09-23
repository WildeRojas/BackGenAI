from django.urls import path, include
from rest_framework import routers
from Apps.projects.viewsets.proyecto_viewset import ProyectoViewSet
from Apps.projects.viewsets.collab_session_viewset import CollabSessionViewSet
from Apps.projects.viewsets.member_session_viewset import MemberSessionViewSet

router = routers.DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
router.register(r'collab-sessions', CollabSessionViewSet)
router.register(r'Member-sessions', MemberSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


