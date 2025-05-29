from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
from django.conf import settings
import os
import pandas as pd

from ..models import Category, BrandFeature, BrandFeatureOption, Brand, BrandFeatureValue, Search, BrandAnalysis
from ..serializers import CategorySerializer, BrandFeatureSerializer
from ..utils.credits import deduct_filtered_credits


@api_view(['GET'])
def get_filters(request):
	"""
	Tüm kategorileri, marka özelliklerini ve özellik seçeneklerini döndüren API.
	"""
	categories = Category.objects.all()
	brand_features = BrandFeature.objects.prefetch_related('options').all()  # Marka özellikleri ve ilişkili seçenekleri getirir.

	category_serializer = CategorySerializer(categories, many=True)
	feature_serializer = BrandFeatureSerializer(brand_features, many=True)

	return Response({
		"categories": category_serializer.data,
		"brand_features": feature_serializer.data  # Seçenekler de bu JSON içinde gelecek.
	})
 
class BrandFilterAPIView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		filters = request.data
		category_ids = filters.get("categories", [])
		feature_value_ids = filters.get("feature_values", [])
		limit = int(filters.get("limit", 50))  # 🔥 Default 50
		offset = int(filters.get("offset", 0))  # 🔥 Default 0

		# Özellik gruplama
		feature_value_groups = {}
		for feature_value_id in feature_value_ids:
			feature_option = BrandFeatureOption.objects.filter(id=feature_value_id).first()
			if feature_option:
				feature_id = feature_option.feature.id
				feature_value_groups.setdefault(feature_id, set()).add(feature_value_id)

		queryset = Brand.objects.filter(categories__id__in=category_ids).distinct()

		filtered_brands = []
		for brand in queryset:
			brand_categories = set(brand.categories.values_list("id", flat=True))
			brand_feature_values = set(brand.feature_values.values_list("feature_option_id", flat=True))

			if not brand_categories.intersection(set(category_ids)):
				continue

			if feature_value_groups:
				feature_check = all(
					brand_feature_values.intersection(value_ids)
					for value_ids in feature_value_groups.values()
				)
				if not feature_check:
					continue

			filtered_brands.append(brand)

		total_count = len(filtered_brands)  # 🔢 Tüm eşleşenlerin sayısı

		# 🔥 Sadece istenen kısmı al
		sliced_brands = filtered_brands[offset:offset + limit]

		if not deduct_filtered_credits(request.user, len(sliced_brands)):
			return Response({"error": "Yetersiz FİLTRELİ sorgu kredisi."}, status=status.HTTP_403_FORBIDDEN)

		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		output_dir = settings.MEDIA_ROOT
		os.makedirs(output_dir, exist_ok=True)
		file_name = f"filtered_analysis_{timestamp}.xlsx"
		file_path = os.path.join(output_dir, file_name)

		search_instance = Search.objects.create(
			query=", ".join([brand.name for brand in sliced_brands]),
			user=request.user,
			excel_link=f"{settings.MEDIA_URL}{file_name}"
		)

		all_results = []
		for brand in sliced_brands:
			result = {
				"brand_name": brand.name,
				"official_site": brand.official_site,
				"emails": brand.emails.split(", ") if brand.emails else [],
				"phone_numbers": brand.phone_numbers.split(", ") if brand.phone_numbers else []
			}
			all_results.append(result)

			BrandAnalysis.objects.create(
				search=search_instance,
				brand_name=brand.name,
				official_site=brand.official_site,
				emails=brand.emails,
				phone_numbers=brand.phone_numbers
			)

		df = pd.DataFrame([
			{
				"Brand Name": res["brand_name"],
				"Official Site": res["official_site"] or "Bulunamadı",
				"Emails": ", ".join(res["emails"]) if res["emails"] else "Bulunamadı",
				"Phone Numbers": ", ".join(res["phone_numbers"]) if res["phone_numbers"] else "Bulunamadı",
			}
			for res in all_results
		])
		df.to_excel(file_path, index=False)

		return Response({
			"results": all_results,
			"excel_download_link": f"{settings.MEDIA_URL}{file_name}",
			"total_count": total_count,  # 🔥 Frontend burada kaç tane daha olduğunu bilir
			"returned_count": len(all_results),
			"offset": offset,
			"limit": limit,
		}, status=status.HTTP_200_OK)