from backend.users.auth_services import token_for_user_with
from django.core.exceptions import PermissionDenied
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class AuthTokenView(APIView):
    class AuthenticationSerializer(serializers.Serializer):
        username = serializers.SlugField(required=True)
        password = serializers.CharField(required=True)

    def _validate_data(self, post_data):
        auth_serializer = self.AuthenticationSerializer(data=post_data)
        auth_serializer.is_valid(raise_exception=True)
        return auth_serializer.validated_data

    def post(self, request):
        try:
            validated_auth_data = self._validate_data(request.POST)
            token = token_for_user_with(**validated_auth_data)
            return Response({"token": token}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
