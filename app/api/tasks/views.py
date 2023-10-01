from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TasksList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class TasksListSerializer(serializers.Serializer):
        title = serializers.CharField()
        created = serializers.DateTimeField()
        expires = serializers.DateTimeField()
        status = serializers.CharField()

    def get(self, request):
        tasks_data = [
            {
                "title": "",
                "created": "",
                "expires": "",
                "status": "",
            },
        ]
        return Response(
            self.TasksListSerializer(tasks_data, many=True).data,
            status=status.HTTP_200_OK,
        )
