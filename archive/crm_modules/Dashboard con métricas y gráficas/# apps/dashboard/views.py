# apps/dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.clients.models import Client
from apps.opportunities.models import Opportunity
from apps.tasks.models import Task
from django.utils.timezone import now, timedelta

class DashboardMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_clients = Client.objects.count()
        total_opportunities = Opportunity.objects.count()
        open_opportunities = Opportunity.objects.filter(status='open').count()
        completed_tasks = Task.objects.filter(status='completed').count()

        # Ejemplo de datos de oportunidades por semana
        last_7_days = now() - timedelta(days=7)
        weekly_opportunities = Opportunity.objects.filter(created_at__gte=last_7_days).count()

        data = {
            'total_clients': total_clients,
            'total_opportunities': total_opportunities,
            'open_opportunities': open_opportunities,
            'completed_tasks': completed_tasks,
            'weekly_opportunities': weekly_opportunities
        }
        return Response(data)
