from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


# Create your models here.

class ProductoBancario(models.Model):
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-fecha']),
            models.Index(fields=['banco'])
        ]


class CDT(models.Model):
    producto_bancario = models.OneToOneField('ProductoBancario', on_delete=models.CASCADE)
    plazo_min_dias = models.IntegerField()
    tasa = models.FloatField()
    monto = models.IntegerField(null=True)
    monto_minimo = models.IntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['-tasa']),
            models.Index(fields=['plazo_min_dias']),
            models.Index(fields=['monto']),
            models.Index(fields=['monto_minimo']),
        ]

    @property
    def banco(self):
        return self.producto_bancario.banco_id

    def __str__(self):
        return "%s: p%d -> t%.2f" % (self.banco, self.plazo_min_dias, self.tasa)


class Banco(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)
    logoCuadrado = models.URLField(null=True)
    logoGrande = models.URLField(null=True)
    slug = models.SlugField(default=nombre)


class CalificacionBanco(models.Model):
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE)
    puntaje = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(5)))
    comentario = models.CharField(max_length=1000)
    fecha = models.DateField(auto_now_add=True)


class CalificacionProducto(models.Model):
    producto = models.ForeignKey('ProductoBancario', on_delete=models.CASCADE)
    puntaje = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(5)))
    comentario = models.CharField(max_length=1000)
    fecha = models.DateField(auto_now_add=True)


class DatosRegistro(models.Model):
    email = models.EmailField(primary_key=True)
    nombre = models.CharField(max_length=50)
    acepta = models.BooleanField()
    telefono = models.CharField(max_length=15, null=True)
    slug_name = models.SlugField(unique=True, max_length=100)
