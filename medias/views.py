from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from .models import Photo


# Create your views here.
class PhotoDetial(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            photo = Photo.objects.get(pk=pk)
            return photo
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.room:
            if photo.room.owner != request.user:
                raise PermissionDenied
        elif photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


class GetUploadURL(APIView):
    def post(self, request):
        return Response(status=HTTP_200_OK)
