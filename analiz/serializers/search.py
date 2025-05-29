from rest_framework import serializers
from ..models import Search, BrandAnalysis
from .brand import BrandAnalysisSerializer  # reuse edildi

class SearchSerializer(serializers.ModelSerializer):
    brand_analyses = BrandAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = Search
        fields = [
            'id',
            'query',
            'excel_link',
            'created_at',
            'brand_analyses'
        ]
