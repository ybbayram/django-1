from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import SubscriptionPlan
from ..serializers import SubscriptionPlanSerializer

class SubscriptionPlanListAPIView(APIView):
    permission_classes = []  # Herkes erişebilir

    def get(self, request):
        plans = SubscriptionPlan.objects.all().order_by("price")  # Fiyat sırasına göre
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
