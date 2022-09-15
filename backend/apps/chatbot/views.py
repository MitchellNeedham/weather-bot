from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.chatbot.utils import get_weather_response_messages, get_client_ip
from weatherbot import settings

from apps.chatbot.models import Conversation, Message
from apps.chatbot.enum import RequestedAction


class ConversationStartAPIView(APIView):
    def get(self, request: Request):
        try:
            new_conversation = Conversation()
            new_conversation.ip = get_client_ip(request)
            new_conversation.save()
            return Response(
                {
                    "conversation_id": new_conversation.id,
                    "messages": [
                        "Hi there!",
                        "I'm a weather bot, please ask me about the weather.",
                        "It's my only purpose."
                    ]
                }
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


class MessageHandlerAPIView(APIView):
    def post(self, request: Request):
        try:
            conversation = Conversation.objects.get(id=request.data.get("conversation_id"))
            message = request.data.get("message", "")

            action = None

            asked_about_weather = settings.CLASSIFIER(message, ["weather"])["scores"][0] > 0.8

            if asked_about_weather:
                if not conversation.latitude or not conversation.longitude:
                    action = RequestedAction.GEO_LOC
                    response = ["I'd love to tell you! But first, I need to know where you are."]
                else:
                    response = get_weather_response_messages(conversation)
            else:
                response = ["I'm not sure, sorry. I'm just a weather bot."]

            Message(
                conversation_id=conversation.id,
                message=message,
                response=response,
                action_requested=action
            ).save()

            return Response({"messages": response, "action": action.value if action else ""})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


class GeolocationAPIView(APIView):
    def post(self, request: Request):
        try:
            conversation = Conversation.objects.get(id=request.data.get("conversation_id"))

            conversation.latitude = request.data.get("latitude", settings.DEFAULT_LATITUDE)
            conversation.longitude = request.data.get("longitude", settings.DEFAULT_LONGITUDE)
            conversation.save()

            messages = get_weather_response_messages(conversation, request.data.get("failed", False))

            print(messages)

            return Response(
                {"messages": messages}
            )
        except Conversation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "conversation_does_not_exist"})
