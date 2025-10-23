# predictor/urls.py
from django.urls import path
from .views import PredictHousePriceView, HealthCheckView

urlpatterns = [
    path('predict/', PredictHousePriceView.as_view(), name='predict-house-price'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]