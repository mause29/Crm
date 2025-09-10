from django.urls import path
from . import views

urlpatterns = [
    path('facturas/', views.panel_facturas, name='panel_facturas'),
    path('factura/<int:factura_id>/orden/', views.crear_orden, name='crear_orden'),
    path('factura/<int:factura_id>/capturar/', views.capturar_pago, name='capturar_pago'),
]
