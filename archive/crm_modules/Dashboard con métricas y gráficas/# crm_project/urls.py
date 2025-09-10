# crm_project/urls.py (agregar)
from apps.dashboard.views import DashboardMetricsView

urlpatterns += [
    path('api/dashboard/', DashboardMetricsView.as_view(), name='dashboard_metrics')
]
