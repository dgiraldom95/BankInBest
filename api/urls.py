from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework.authtoken import views as authtoken_views

router = DefaultRouter()
router.register(r'CDTs', views.CDTViewSet)
router.register(r'calificaciones-productos', views.CalificacionProductoViewSet)
router.register(r'calificaciones-bancos', views.CalificacionBancoViewSet)
router.register(r'datos-registro', views.DatosRegistroViewSet)
router.register(r'bancos', views.BancoViewSet)
router.register(r'usuarios', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', authtoken_views.obtain_auth_token, name='api-token-auth')
]
