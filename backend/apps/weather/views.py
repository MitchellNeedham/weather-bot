from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from weatherbot.settings import GEOIP_PATH


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


class WeatherAPIView(APIView):
    def get(self, request):
        g = GeoIP2("/usr/src/server/weatherbot/geodat/GeoLite2-City.mmdb")
        ip = get_client_ip(request)
        try:
            city = g.city('google.com')
        except Exception:
            city = 'Failed'
        return Response({"city": city, "ip": ip})
