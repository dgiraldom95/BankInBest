from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import *
import unidecode


class BancoSerializer(serializers.ModelSerializer):
    calificacion_promedio = serializers.ReadOnlyField()

    class Meta:
        model = Banco
        fields = ('nombre', 'calificacion_promedio', 'puntaje_bankinbest', 'slug', 'logoCuadrado', 'logoGrande')
        read_only_fields = ('slug',)

    def nameToSlug(self, name):
        slug = name.replace(' ', '-')
        slug = unidecode.unidecode(slug)
        return slug

    def to_internal_value(self, data):
        ret = super(BancoSerializer, self).to_internal_value(data)
        ret['slug'] = self.nameToSlug(ret['nombre'])
        return ret


class ProductoBancarioSerializer(serializers.HyperlinkedModelSerializer):
    banco = BancoSerializer(read_only=True)

    class Meta:
        model = ProductoBancario
        fields = ('id', 'banco',)


class CDTSerializer(serializers.ModelSerializer):
    banco = serializers.CharField()
    producto_bancario = ProductoBancarioSerializer(read_only=True)

    class Meta:
        model = CDT
        fields = ('id', 'plazo_min_dias', 'tasa', 'monto', 'monto_minimo', 'banco', 'producto_bancario')

    def create(self, validated_data):
        banco = validated_data.get('banco')
        plazoMinDias = validated_data.get('plazo_min_dias')
        tasa = validated_data.get('tasa')
        montoMinimo = validated_data.get('monto_minimo')
        monto = validated_data.get('monto')

        producto = ProductoBancario.objects.create(banco_id=banco)
        cdt = CDT.objects.create(plazo_min_dias=plazoMinDias, tasa=tasa, monto_minimo=montoMinimo,
                                 producto_bancario=producto, monto=monto)
        return cdt


class CalificacionBancoSerializer(serializers.ModelSerializer):
    fecha = serializers.ReadOnlyField()

    class Meta:
        model = CalificacionBanco
        fields = '__all__'
        read_only_fields = ('banco', 'usuario')

    def create(self, validated_data):
        data = {**self.context, **validated_data}
        return CalificacionBanco.objects.create(**data)


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


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(email, password, **validated_data)
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'nombre', 'apellido', 'ciudad', 'fecha_nacimiento', 'telefono')
