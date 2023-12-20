from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
conn = get_redis_connection("monitor")


class GetTasks(APIView):
    permission_classes = []

    def get(self, request):
        server_uuid = request.query_params.get('uuid')
        return HttpResponse(conn.get('task_{}'.format(server_uuid)), content_type="application/json")
