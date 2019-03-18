from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api.serializers import *
from api.models import *
from rest_framework.decorators import action


class CDTViewSet(viewsets.ModelViewSet):
    queryset = CDT.objects.all()
    serializer_class = CDTSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=True)
    def calificaciones(self, request, pk=None):
        cdt = CDT.objects.get(pk=pk)
        calificacionesModel = CalificacionProducto.objects.filter(producto=cdt.productoBancario_id)
        calificacionSerializer = CalificacionProductoSerializer(calificacionesModel, many=True)
        return Response(calificacionSerializer.data)

    @calificaciones.mapping.post
    def postCalificaciones(self, request, pk=None):
        request.data['producto'] = pk
        serializer = CalificacionProductoSerializer(data=request.data)
        if serializer.is_valid():
            calificacion = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalificacionBancoViewSet(viewsets.ModelViewSet):
    queryset = CalificacionBanco.objects.all()
    serializer_class = CalificacionBancoSerializer
    permission_classes = (permissions.AllowAny,)


class CalificacionProductoViewSet(viewsets.ModelViewSet):
    queryset = CalificacionProducto.objects.all()
    serializer_class = CalificacionProductoSerializer
    permission_classes = (permissions.AllowAny,)


class DatosRegistroViewSet(viewsets.ModelViewSet):
    queryset = DatosRegistro.objects.all()
    serializer_class = DatosRegistroSerializer
    permission_classes = (permissions.AllowAny,)
