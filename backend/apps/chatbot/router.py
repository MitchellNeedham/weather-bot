from django.urls import path

from apps.chatbot.views import MessageHandlerAPIView, ConversationStartAPIView, GeolocationAPIView

urlpatterns = [
    path("conversation/message-handler", MessageHandlerAPIView.as_view(), name="message-handler"),
    path("conversation/start-conversation", ConversationStartAPIView.as_view(), name="message-handler"),
    path("conversation/set-location", GeolocationAPIView.as_view(), name="message-handler"),
]
