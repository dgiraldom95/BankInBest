from rest_framework import serializers
from api.models import *


class CDTSerializer(serializers.ModelSerializer):
    banco = serializers.CharField()

    class Meta:
        model = CDT
        fields = ('id', 'plazoMinDias', 'tasa', 'montoMinimo', 'banco')

    def create(self, validated_data):
        banco = validated_data.get('banco')
        plazoMinDias = validated_data.get('plazoMinDias')
        tasa = validated_data.get('tasa')
        montoMinimo = validated_data.get('montoMinimo')

        producto = ProductoBancario.objects.create(banco_id=banco)
        cdt = CDT.objects.create(plazoMinDias=plazoMinDias, tasa=tasa, montoMinimo=montoMinimo,
                                 productoBancario=producto)
        return cdt


class CalificacionBancoSerializer(serializers.ModelSerializer):
    fecha = serializers.ReadOnlyField()

    class Meta:
        model = CalificacionBanco
        fields = '__all__'


class CalificacionProductoSerializer(serializers.ModelSerializer):
    fecha = serializers.ReadOnlyField()

    class Meta:
        model = CalificacionProducto
        fields = '__all__'
