# crm_project/urls.py
from apps.billing.views import PayPalCreateOrderView, PayPalCaptureOrderView

urlpatterns += [
    path('api/billing/paypal/create-order/', PayPalCreateOrderView.as_view(), name='paypal_create_order'),
    path('api/billing/paypal/capture-order/', PayPalCaptureOrderView.as_view(), name='paypal_capture_order'),
]
