from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class JwtView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Only authenticated users can access this endpoint
        content = {"message": "Hello, you're authenticated!"}
        return Response(content)
