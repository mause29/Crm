# Analytics
def kpi_report():
    from analytics.models import KPI
    return KPI.objects.all().order_by('-date')[:30]
