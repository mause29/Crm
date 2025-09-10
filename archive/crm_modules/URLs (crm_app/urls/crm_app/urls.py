from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('clientes', views.ClienteViewSet)
router.register('oportunidades', views.OportunidadViewSet)
router.register('tareas', views.TareaViewSet)
router.register('facturas', views.FacturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('facturas/panel/', views.panel_facturas, name='panel_facturas'),
    path('factura/<int:factura_id>/orden/', views.crear_orden, name='crear_orden'),
    path('factura/<int:factura_id>/capturar/', views.capturar_pago, name='capturar_pago'),
]
