from django.utils.text import slugify
from rest_framework import serializers
from api.models import *
import unidecode


class BancoSerializer(serializers.ModelSerializer):
    calificacion_promedio = serializers.ReadOnlyField()

    class Meta:
        model = Banco
        fields = ('nombre', 'calificacion_promedio', 'slug', 'logoCuadrado', 'logoGrande')
        read_only_fields = ('slug',)

    def nameToSlug(self, name):
        slug = name.replace(' ', '-')
        slug = unidecode.unidecode(slug)
        return slug

    def to_internal_value(self, data):
        ret = super(BancoSerializer, self).to_internal_value(data)
        ret['slug'] = self.nameToSlug(ret['nombre'])
        return ret


class ProductoBancarioSerializer(serializers.ModelSerializer):
    banco = BancoSerializer(read_only=True)

    class Meta:
        model = ProductoBancario
        fields = ('id', 'banco',)


class CDTSerializer(serializers.ModelSerializer):
    banco = serializers.CharField()
    producto_bancario = ProductoBancarioSerializer(read_only=True)

    class Meta:
        model = CDT
        fields = ('id', 'plazo_min_dias', 'tasa', 'monto_minimo', 'banco', 'producto_bancario')

    def create(self, validated_data):
        banco = validated_data.get('banco')
        plazoMinDias = validated_data.get('plazo_min_dias')
        tasa = validated_data.get('tasa')
        montoMinimo = validated_data.get('monto_minimo')

        producto = ProductoBancario.objects.create(banco_id=banco)
        cdt = CDT.objects.create(plazo_min_dias=plazoMinDias, tasa=tasa, monto_minimo=montoMinimo,
                                 producto_bancario=producto)
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
