# Generated by Django 2.1.7 on 2019-03-31 01:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('nombre', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('logoCuadrado', models.URLField(null=True)),
                ('logoGrande', models.URLField(null=True)),
                ('slug', models.SlugField(default=models.CharField(max_length=50, primary_key=True, serialize=False))),
            ],
        ),
        migrations.CreateModel(
            name='CalificacionBanco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comentario', models.CharField(max_length=1000)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Banco')),
            ],
        ),
        migrations.CreateModel(
            name='CalificacionProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comentario', models.CharField(max_length=1000)),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CDT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plazo_min_dias', models.IntegerField()),
                ('tasa', models.FloatField()),
                ('monto', models.IntegerField(null=True)),
                ('monto_minimo', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DatosRegistro',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('acepta', models.BooleanField()),
                ('telefono', models.CharField(max_length=15, null=True)),
                ('slug_name', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoBancario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Banco')),
            ],
        ),
        migrations.AddField(
            model_name='cdt',
            name='producto_bancario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.ProductoBancario'),
        ),
        migrations.AddField(
            model_name='calificacionproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ProductoBancario'),
        ),
        migrations.AddIndex(
            model_name='productobancario',
            index=models.Index(fields=['-fecha'], name='api_product_fecha_cdb57e_idx'),
        ),
        migrations.AddIndex(
            model_name='productobancario',
            index=models.Index(fields=['banco'], name='api_product_banco_i_95fa13_idx'),
        ),
        migrations.AddIndex(
            model_name='cdt',
            index=models.Index(fields=['-tasa'], name='api_cdt_tasa_80d317_idx'),
        ),
        migrations.AddIndex(
            model_name='cdt',
            index=models.Index(fields=['plazo_min_dias'], name='api_cdt_plazo_m_3486ee_idx'),
        ),
        migrations.AddIndex(
            model_name='cdt',
            index=models.Index(fields=['monto'], name='api_cdt_monto_bf295b_idx'),
        ),
        migrations.AddIndex(
            model_name='cdt',
            index=models.Index(fields=['monto_minimo'], name='api_cdt_monto_m_11e1ad_idx'),
        ),
    ]
