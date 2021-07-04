from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'', views.PaymentsViewSet, basename='payments')

urlpatterns = router.urls