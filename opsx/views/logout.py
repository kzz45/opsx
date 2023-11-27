from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Logout(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
