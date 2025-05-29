from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    official_site = models.URLField(max_length=500, null=True, blank=True)
    emails = models.TextField(null=True, blank=True)
    phone_numbers = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name="brands", blank=True)

    def __str__(self):
        return self.name


class BrandAnalysis(models.Model):
    search = models.ForeignKey("Search", on_delete=models.CASCADE, related_name="brand_analyses")
    brand_name = models.CharField(max_length=255)
    official_site = models.URLField(max_length=500, null=True, blank=True)
    emails = models.TextField(null=True, blank=True)
    phone_numbers = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name


class BrandFeature(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BrandFeatureOption(models.Model):
    feature = models.ForeignKey(BrandFeature, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('feature', 'value')

    def __str__(self):
        return f"{self.feature.name}: {self.value}"


class BrandFeatureValue(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="feature_values")
    feature_option = models.ForeignKey(BrandFeatureOption, on_delete=models.CASCADE, related_name="brand_values", null=True, blank=True)

    class Meta:
        unique_together = ('brand', 'feature_option')

    def __str__(self):
        return f"{self.brand.name} - {self.feature_option.feature.name}: {self.feature_option.value}" if self.feature_option else f"{self.brand.name} - Özellik Yok"