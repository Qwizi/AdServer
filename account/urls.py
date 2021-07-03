from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register(r'ads', views.AccountAdViewSet)

ads_stats_view_router = routers.NestedSimpleRouter(router, r'ads', lookup='ad')
ads_stats_view_router.register(r'view-stats', views.AccountAdStatsViewViewSet, basename='ad-view-stats')
ads_stats_view_router.register(r'click-stats', views.AccountAdStatsClickViewSet, basename='ad-click-stats')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(ads_stats_view_router.urls))
]