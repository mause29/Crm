from django.urls import path
from . import views

urlpatterns = [
    path('factura/crear/', views.crear_factura, name='crear_factura'),
    path('factura/<int:factura_id>/orden/', views.crear_orden, name='crear_orden'),
    path('factura/<int:factura_id>/capturar/', views.capturar_pago, name='capturar_pago'),
]
