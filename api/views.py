from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api.serializers import *
from api.models import *
from rest_framework.decorators import action
import datetime
from django.db.models import prefetch_related_objects


class CDTViewSet(viewsets.ModelViewSet):
    queryset = CDT.objects.order_by('-tasa')
    queryset = queryset.filter()
    serializer_class = CDTSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        params = self.request.query_params

        monto = params['monto']
        plazo = params['plazo']
        fecha = datetime.datetime.today().strftime('%Y-%m-%d')

        sql = """ SELECT api_cdt.id, api_cdt.plazo_min_dias, api_cdt.tasa, api_cdt.monto, api_cdt.monto_minimo, api_cdt.producto_bancario_id
                    FROM api_cdt,  
                            api_productobancario productobancario,
                            (SELECT prod.banco_id banco, max(cdt.tasa) tasa
                                FROM api_cdt cdt,
                                    api_productobancario prod
                                WHERE (
                                 (cdt.monto_minimo <= %s OR cdt.monto_minimo IS NULL)
                                   AND (cdt.monto <= %s OR monto IS NULL)
                                   AND (cdt.producto_bancario_id = prod.id)
                                   AND (cdt.plazo_min_dias <= %s)
                                   AND (prod.fecha = %s)
                                    )
                                GROUP BY prod.banco_id
                            ) maxTasa
                    WHERE api_cdt.tasa = maxTasa.tasa
                       AND api_cdt.producto_bancario_id = productobancario.id
                       AND productobancario.banco_id = maxTasa.banco
                    ORDER BY api_cdt.tasa DESC;
             """

        query = CDT.objects.raw(sql, params=[monto, monto, plazo, fecha])
        prefetch_related_objects(query, 'producto_bancario')
        prefetch_related_objects(query, 'producto_bancario__banco')

        dicNoRepetir = {}
        listaFinal = []
        for cdt in query:
            if cdt.banco not in dicNoRepetir:
                dicNoRepetir[cdt.banco] = True
                listaFinal.append(cdt)

        serializer = self.get_serializer(listaFinal, many=True)
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
