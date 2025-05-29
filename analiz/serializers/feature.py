from rest_framework import serializers
from ..models import BrandFeature, BrandFeatureOption

class BrandFeatureOptionSerializer(serializers.ModelSerializer):
    """ Marka özelliklerine ait seçenekleri döndürür """
    class Meta:
        model = BrandFeatureOption
        fields = ['id', 'value']


class BrandFeatureSerializer(serializers.ModelSerializer):
    """ Marka özelliklerini ve ilişkili tüm seçeneklerini döndürür """
    options = BrandFeatureOptionSerializer(many=True, read_only=True)

    class Meta:
        model = BrandFeature
        fields = ['id', 'name', 'options']
