from rest_framework.views import APIView
from rest_framework.response import Response


class MessageHandlerApiView(APIView):
    def post(self, request):
        return Response({"data": "hello"})
