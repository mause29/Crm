# crm_project/urls.py (agregar)
from apps.billing.views import CreatePaymentIntentView

urlpatterns += [
    path('api/billing/create-intent/', CreatePaymentIntentView.as_view(), name='create_payment_intent')
]
