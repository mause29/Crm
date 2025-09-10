# apps/opportunities/views.py
from rest_framework import viewsets
from .models import Opportunity
from .serializers import OpportunitySerializer
from rest_framework.permissions import IsAuthenticated

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]
