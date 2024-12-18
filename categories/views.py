from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomCategories(APIView):
    def get(self, request):
        all_room_categories = Category.objects.filter(
            kind=Category.CategoryKindChoices.ROOMS,
        )
        serializer = CategorySerializer(all_room_categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        # raise가 발생되면 뒤의 코드 작동 안한다

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(HTTP_204_NO_CONTENT)
