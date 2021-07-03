from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register(r'ads', views.AccountAdViewSet)
router.register(r'orders', views.AccountOrdersViewSet)

ads_stats_view_router = routers.NestedSimpleRouter(router, r'ads', lookup='ad')
ads_stats_view_router.register(r'views', views.AccountAdStatsViewViewSet, basename='ad-views')
ads_stats_view_router.register(r'clicks', views.AccountAdStatsClickViewSet, basename='ad-clicks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(ads_stats_view_router.urls))
]