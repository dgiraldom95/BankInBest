from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'CDTs', views.CDTViewSet)
router.register(r'calificaciones-productos', views.CalificacionProductoViewSet)
router.register(r'calificaciones-bancos', views.CalificacionBancoViewSet)
router.register(r'datos-registro', views.DatosRegistroViewSet)

urlpatterns = [
    path('', include(router.urls))
]
