from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
from django.db.models import F
from django.template.defaultfilters import slugify


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
    slug = models.SlugField(default=nombre, unique=True)
    puntaje_total = models.FloatField(default=0)
    puntaje_bankinbest = models.FloatField(default=0)
    numero_calificaciones = models.BigIntegerField(default=0)

    @property
    def calificacion_promedio(self):
        if self.numero_calificaciones > 0:
            return self.puntaje_total / self.numero_calificaciones
        else:
            return 0


class CalificacionBanco(models.Model):
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE)
    puntaje = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(5)))
    comentario = models.CharField(max_length=1000)
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    class CalificacionBancoManager(models.Manager):
        def create(self, **kwargs):
            calificacion = super(CalificacionBanco.CalificacionBancoManager, self).create(**kwargs)
            banco = calificacion.banco
            banco.numero_calificaciones = F('numero_calificaciones') + 1
            banco.puntaje_total = F('puntaje_total') + calificacion.puntaje
            banco.save()
            return calificacion

    objects = CalificacionBancoManager()


class CalificacionProducto(models.Model):
    producto = models.ForeignKey('ProductoBancario', on_delete=models.CASCADE)
    puntaje = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(5)))
    comentario = models.CharField(max_length=1000)
    fecha = models.DateField(auto_now_add=True)


class DatosRegistro(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    acepta = models.BooleanField()
    telefono = models.CharField(max_length=15, null=True)
    slug_name = models.SlugField(unique=True, max_length=100)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **kwargs):
        nombre = None
        apellido = None
        telefono = None
        fecha_nacimiento = None
        ciudad = None

        if 'nombre' in kwargs:
            nombre = kwargs['nombre']
        if 'apellido' in kwargs:
            apellido = kwargs['apellido']
        if 'telefono' in kwargs:
            telefono = kwargs['telefono']
        if 'fecha_nacimiento' in kwargs:
            fecha_nacimiento = kwargs['fecha_nacimiento']
        if 'ciudad' in kwargs:
            ciudad = kwargs['ciudad']

        slug = email.replace('.', '_')
        slug = slugify(slug)

        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            ciudad=ciudad,
            slug=slug
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=20, null=True)
    fecha_nacimiento = models.DateField(null=True)
    ciudad = models.CharField(max_length=50, null=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    objects = UserManager()
