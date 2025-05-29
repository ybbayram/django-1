from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.analysis import MarkaAnalizAPIView
from .views.filters import get_filters, BrandFilterAPIView
from .views.search import UserSearchListAPIView, TopSearchedBrandsAPIView
from .views.stats import UserStatsAPIView
from .views.subscription import SubscriptionPlanListAPIView

urlpatterns = [
    path('marka-analiz/', MarkaAnalizAPIView.as_view(), name='marka-analiz'),
    path('user-searches/', UserSearchListAPIView.as_view(), name='user-searches'),
    path('filtreler/', get_filters, name='get_filters'),
    path('marka-analiz-filter/', BrandFilterAPIView.as_view(), name='brand-filter'),
    path('user-stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('plans/', SubscriptionPlanListAPIView.as_view(), name='subscription-plans'),
    path('top-brands/', TopSearchedBrandsAPIView.as_view(), name='top-brands'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
