from django.db import models


# Create your models here.
class CDT(models.Model):
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE)
    plazoMin = models.IntegerField()
    tasa = models.FloatField()
    montoMinimoDias = models.IntegerField()


class Banco(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)