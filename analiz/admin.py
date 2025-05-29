from django.contrib import admin
from .models import (
    Search, Brand, BrandFeature, BrandFeatureValue, BrandAnalysis,
    Category, BrandFeatureOption, SubscriptionPlan, UserSubscription
)
from django.utils.translation import gettext_lazy as _

# 📌 Yönetici paneli başlıklarını güncelle
admin.site.site_header = _("Proje Yönetici Paneli")
admin.site.site_title = _("Proje Admin")
admin.site.index_title = _("Proje Yönetim Paneline Hoş Geldiniz")


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'query', 'user', 'created_at')
    search_fields = ('query', 'user__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'official_site', 'created_at')
    search_fields = ('name', 'official_site')
    list_filter = ('created_at', 'categories')
    ordering = ('-created_at',)
    filter_horizontal = ('categories',)


@admin.register(BrandFeature)
class BrandFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(BrandFeatureOption)
class BrandFeatureOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'feature', 'value')
    search_fields = ('feature__name', 'value')
    list_filter = ('feature',)
    ordering = ('feature', 'value')


@admin.register(BrandFeatureValue)
class BrandFeatureValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'feature_option')
    search_fields = ('brand__name', 'feature_option__feature__name', 'feature_option__value')
    list_filter = ('feature_option__feature',)
    ordering = ('brand',)


@admin.register(BrandAnalysis)
class BrandAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand_name', 'official_site', 'search', 'created_at')
    search_fields = ('brand_name', 'official_site')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


# ✅ GÜNCEL: Abonelik Paketleri (SubscriptionPlan)
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'basic_brand_credits', 'filtered_brand_credits', 'payment_url')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('price',)



# ✅ GÜNCEL: Kullanıcı Abonelikleri (UserSubscription)
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'plan',
        'remaining_basic_credits', 'remaining_filtered_credits',
        'created_at', 'expires_at'
    )
    search_fields = ('user__username', 'plan__name')
    list_filter = ('plan', 'created_at')
    ordering = ('-created_at',)
