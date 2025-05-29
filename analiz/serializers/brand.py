from rest_framework import serializers
from ..models import BrandAnalysis, Brand, BrandFeatureValue, Category

# 1. BrandAnalysis sonuçlarını dönen serializer
class BrandAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandAnalysis
        fields = ['id', 'brand_name', 'official_site', 'emails', 'phone_numbers', 'created_at']


# 2. Özellik değerlerini dönen serializer (markaya ait değerler)
class FeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandFeatureValue
        fields = ['id', 'feature_option']


# 3. Kategori bilgisi (Brand içinde ilişkili geliyor)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# 4. Marka detaylarını tüm alanlarıyla dönen serializer
class BrandDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    feature_values = FeatureValueSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'official_site',
            'emails',
            'phone_numbers',
            'categories',
            'feature_values',
        ]
