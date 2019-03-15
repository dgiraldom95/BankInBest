from rest_framework import serializers
from api.models import *


class CDTSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDT
        fields = '__all__'
