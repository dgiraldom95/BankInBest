from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *
from api.models import *
from rest_framework.decorators import action
import datetime
from django.db.models import prefetch_related_objects
import api.permissions


class CDTViewSet(viewsets.ModelViewSet):
    queryset = CDT.objects.order_by('-tasa')
    queryset = queryset.filter()
    serializer_class = CDTSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        params = self.request.query_params

        if 'monto' in params and 'plazo' in params:
            monto = params['monto']
            plazo = params['plazo']

            sql = """ WITH cdtsCand AS (SELECT api_productobancario.banco_id banco, cdtsPosibles.id idcdt, *
                                          FROM api_productobancario,
                                               (SELECT banco_id, max(fecha) fecha FROM api_productobancario GROUP BY banco_id) ultimaFecha,
                                               (SELECT *
                                                FROM api_cdt
                                                WHERE (api_cdt.monto_minimo <= %s or monto_minimo IS NULL)
                                                  AND (api_cdt.monto <= %s or api_cdt.monto IS NULL)
                                                  AND (api_cdt.plazo_min_dias <= %s or api_cdt.plazo_min_dias IS NULL)) cdtsPosibles
                                          WHERE api_productobancario.banco_id = ultimaFecha.banco_id
                                            AND api_productobancario.fecha = ultimaFecha.fecha
                                            AND api_productobancario.id = cdtsPosibles.producto_bancario_id)
                    SELECT cdtsCand.idcdt id,
                           cdtsCand.producto_bancario_id,
                           cdtsCand.plazo_min_dias,
                           cdtsCand.tasa,
                           cdtsCand.monto_minimo,
                           cdtsCand.monto
                    FROM cdtsCand,
                         (SELECT cdtsCand.banco, max(tasa) tasa FROM cdtsCand GROUP BY cdtsCand.banco) maxTasas
                    WHERE cdtsCand.tasa = maxTasas.tasa
                      AND cdtsCand.banco = maxTasas.banco
                    ORDER BY cdtsCand.tasa DESC;
                 """

            query = CDT.objects.raw(sql, params=[monto, monto, plazo])
            prefetch_related_objects(query, 'producto_bancario')
            prefetch_related_objects(query, 'producto_bancario__banco')

            dicNoRepetir = {}
            listaFinal = []
            for cdt in query:
                if cdt.banco not in dicNoRepetir:
                    dicNoRepetir[cdt.banco] = True
                    listaFinal.append(cdt)

            serializer = self.get_serializer(listaFinal, many=True)

        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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


class BancoViewSet(viewsets.ModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

    @action(detail=True)
    def calificaciones(self, request, slug=None):
        calificaciones = CalificacionBanco.objects.filter(banco__slug=slug)

        page = self.paginate_queryset(calificaciones)
        if page is not None:
            serializer = CalificacionBancoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CalificacionBancoSerializer(calificaciones, many=True)
        return Response(serializer.data)

    @calificaciones.mapping.post
    def postCalificaciones(self, request, slug=None):

        if not request.user.is_authenticated:
            return Response("Authentication Credentials were not provided.", status.HTTP_401_UNAUTHORIZED)
        else:
            banco = Banco.objects.get(slug=slug)
            if banco is None:
                return Response("Banco no existe", status.HTTP_404_NOT_FOUND)
            # request.data['banco'] = banco.pk
            # request.data['usuario'] = request.user
            serializer = CalificacionBancoSerializer(data=request.data,
                                                     context={'banco': banco, 'usuario': request.user})

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
    lookup_field = 'slug_name'

    @action(detail=True)
    def existe(self, request, slug_name=None):
        response_data = {}
        if DatosRegistro.objects.filter(slug_name=slug_name).exists():
            response_data['existe'] = 'SI'
        else:
            response_data['existe'] = 'NO'
        return Response(response_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (api.permissions.UsernamePermission,)
    lookup_field = 'slug'

    @action(detail=False)
    def calificaciones(self, request, slug=None):
        usuario = request.user
        queryset = CalificacionBanco.objects.filter(usuario=usuario.pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CalificacionBancoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CalificacionBancoSerializer(queryset, many=True)
        return Response(serializer.data)


class Logout(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_400_BAD_REQUEST)
        else:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
