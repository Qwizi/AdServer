from django.urls import path, include
from rest_framework_nested import routers
from django.views.decorators.csrf import csrf_exempt
from . import views

#router = routers.SimpleRouter()
#router.register(r'', views.PaymentsView, basename='payments')

urlpatterns = [
    path("", csrf_exempt(views.PaymentsView.as_view())),
    path("webhook/", csrf_exempt(views.PaymentsWebhookView.as_view()))
]

#urlpatterns += router.urls
