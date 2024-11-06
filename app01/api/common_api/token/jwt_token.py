from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# 用户登录或者携带token可以访问接口，需要使用APIView这个视图
class JwtView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Only authenticated users can access this endpoint
        content = {"message": "Hello, you're authenticated!"}
        return Response(content)
