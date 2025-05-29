from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone

from ..models import UserSubscription, Search

class UserStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        subscription = UserSubscription.objects.filter(user=user).first()
        total_queries = Search.objects.filter(user=user).count()

        if subscription:
            days_left = (subscription.expires_at - datetime.now(timezone.utc)).days
            remaining_basic_credits = subscription.remaining_basic_credits
            remaining_filtered_credits = subscription.remaining_filtered_credits
            subscription_plan = subscription.plan.name
        else:
            days_left = 0
            remaining_basic_credits = 0
            remaining_filtered_credits = 0
            subscription_plan = "Ücretsiz"

        return Response({
            "remaining_basic_credits": remaining_basic_credits,
            "remaining_filtered_credits": remaining_filtered_credits,
            "subscription_plan": subscription_plan,
            "days_left": days_left,
            "total_queries": total_queries
        }, status=status.HTTP_200_OK)
