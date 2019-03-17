from rest_framework import viewsets, permissions
from api.serializers import *
from api.models import *
from rest_framework.decorators import action


class CDTViewSet(viewsets.ModelViewSet):
    queryset = CDT.objects.all()
    serializer_class = CDTSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=True, methods=['post'])
    def post_calificaciones(self, request):
        pass


class CalificacionBancoViewSet(viewsets.ModelViewSet):
    queryset = CalificacionBanco.objects.all()
    serializer_class = CalificacionBancoSerializer
    permission_classes = (permissions.AllowAny,)


class CalificacionProductoViewSet(viewsets.ModelViewSet):
    queryset = CalificacionProducto.objects.all()
    serializer_class = CalificacionProductoSerializer
    permission_classes = (permissions.AllowAny,)
