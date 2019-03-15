from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'CDTs', views.CDTViewSet)

urlpatterns = [
    path('', include(router.urls))
]
