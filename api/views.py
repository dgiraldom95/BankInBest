from rest_framework import viewsets, permissions
from api.serializers import *
from api.models import *

class CDTViewSet(viewsets.ModelViewSet):
    queryset = CDT.objects.all()
    serializer_class = CDTSerializer
    permission_classes = (permissions.AllowAny, )


