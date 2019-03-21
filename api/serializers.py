from django.utils.text import slugify
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


class DatosRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosRegistro
        fields = '__all__'
        read_only_fields = ('slug_name',)

    def emailToSlug(self, email):
        slug = email.replace('.', '%1%')
        slug = slug.replace('@', '%2%')
        return slug

    def to_internal_value(self, data):
        ret = super(DatosRegistroSerializer, self).to_internal_value(data)
        ret['slug_name'] = self.emailToSlug(ret['email'])
        return ret
