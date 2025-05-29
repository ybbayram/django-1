from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime
import os
import pandas as pd
import uuid

from ..models import Search, BrandAnalysis
from ..utils.credits import deduct_basic_credits
from ..utils.brand_analysis import analyze_brand  

class MarkaAnalizAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        brand_names = request.data.get("brand_names")
        if not brand_names:
            return Response({"error": "Marka adları gereklidir."}, status=status.HTTP_400_BAD_REQUEST)

        brand_list = [brand.strip() for brand in brand_names.split(",")]

        if not deduct_basic_credits(request.user, len(brand_list)):
            return Response({"error": "Yetersiz BASIC sorgu kredisi."}, status=status.HTTP_403_FORBIDDEN)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"brand_analysis_{timestamp}_{uuid.uuid4().hex}_data.xlsx"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        search_instance = Search.objects.create(
            query=", ".join(brand_list),
            user=request.user,
            excel_link=f"{settings.MEDIA_URL}{file_name}"
        )

        all_results = []

        for brand_name in brand_list:
            result = analyze_brand(brand_name, search_instance)
            all_results.append(result)

        # Excel dosyası oluştur
        df = pd.DataFrame([
            {
                "Brand Name": r.get("brand_name"),
                "Official Site": r.get("official_site", "Bulunamadı"),
                "Emails": ", ".join(r.get("emails", [])) or "Bulunamadı",
                "Phone Numbers": ", ".join(r.get("phone_numbers", [])) or "Bulunamadı"
            } for r in all_results
        ])
        df.to_excel(file_path, index=False)

        return Response({
            "results": all_results,
            "excel_download_link": f"{settings.MEDIA_URL}{file_name}"
        }, status=status.HTTP_200_OK)
