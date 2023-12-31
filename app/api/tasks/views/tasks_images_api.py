from backend.tasks.services import (
    create_task_image,
    delete_task_image,
    get_task_images_list_for_owner,
)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateTaskImage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class TaskImageSerializer(serializers.Serializer):
        image = serializers.ImageField(required=True)

    def _validate_data(self, data):
        image_serializer = self.TaskImageSerializer(data=data)
        image_serializer.is_valid(raise_exception=True)
        return image_serializer.validated_data

    def post(self, request, task_uuid):
        try:
            image_data = self._validate_data(request.data)
            task_image = create_task_image(
                task_uuid=str(task_uuid),
                owner_id=request.user.id,
                image=image_data.get("image"),
            )
            return Response(
                {"image": task_image.image.url}, status=status.HTTP_201_CREATED
            )
        except (ObjectDoesNotExist, PermissionError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskImage(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_image_uuid):
        try:
            delete_task_image(
                task_image_uuid=str(task_image_uuid), owner_id=request.user.id
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (ObjectDoesNotExist, PermissionError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListTaskImages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class TaskImageSerializer(serializers.Serializer):
        uuid = serializers.UUIDField()
        image = serializers.ImageField()

    def get(self, request, task_uuid):
        try:
            images_list = get_task_images_list_for_owner(
                task_uuid=task_uuid, owner_id=request.user.id
            )
            return Response(
                self.TaskImageSerializer(images_list, many=True).data,
                status=status.HTTP_200_OK,
            )
        except (ObjectDoesNotExist, PermissionError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
