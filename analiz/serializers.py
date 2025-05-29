from rest_framework import serializers
from .models import Search, BrandAnalysis, Category, BrandFeature, BrandFeatureOption, BrandFeatureValue, Brand, SubscriptionPlan

class BrandAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandAnalysis
        fields = ['id', 'brand_name', 'official_site', 'emails', 'phone_numbers', 'created_at']

class SearchSerializer(serializers.ModelSerializer):
    brand_analyses = BrandAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = Search
        fields = ['id', 'query', 'excel_link', 'created_at', 'brand_analyses']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class BrandFeatureOptionSerializer(serializers.ModelSerializer):
    """ Marka özelliklerine ait seçenekleri döndürür """
    class Meta:
        model = BrandFeatureOption
        fields = ['id', 'value']


class BrandFeatureSerializer(serializers.ModelSerializer):
    """ Marka özelliklerini ve olası değerlerini döndürür """
    options = BrandFeatureOptionSerializer(many=True, read_only=True)

    class Meta:
        model = BrandFeature
        fields = ['id', 'name', 'options']
        
class FeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandFeatureValue
        fields = ['id', 'feature_option']


class BrandDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    feature_values = FeatureValueSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'official_site', 'emails', 'phone_numbers', 'categories', 'feature_values']
        

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"  # Tüm alanları döndür