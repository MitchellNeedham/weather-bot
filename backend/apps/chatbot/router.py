from django.urls import path

from apps.chatbot.views import MessageHandlerApiView

urlpatterns = [
    path("weather", MessageHandlerApiView.as_view(), name="custom_map"),
]
