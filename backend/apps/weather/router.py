from django.urls import path

from apps.weather.views import WeatherAPIView

urlpatterns = [
    path("weather", WeatherAPIView.as_view(), name="custom_map"),
]
