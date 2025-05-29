from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from ..models import Search, BrandAnalysis
from ..serializers import SearchSerializer

class UserSearchListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Sadece doğrulanmış kullanıcılar erişebilir

    def get(self, request):
        user = request.user
        user_searches = Search.objects.filter(user=user).order_by('-created_at')
        serializer = SearchSerializer(user_searches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopSearchedBrandsAPIView(APIView):
    permission_classes = []

    def get(self, request):
        top_brands = (
            BrandAnalysis.objects
            .values('brand_name')
            .annotate(search_count=Count('brand_name'))
            .order_by('-search_count')[:5]
        )

        return Response(top_brands, status=status.HTTP_200_OK)
