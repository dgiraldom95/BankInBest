from django.contrib import admin
from api.models import *
from django.apps import apps

# Register your models here.
# Register your models here.
app = apps.get_app_config('api')

for model_name, model in app.models.items():
    admin.site.register(model)