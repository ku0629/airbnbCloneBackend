from rest_framework import serializers

from .models import Perk, Experience
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer, VideoSerializer


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "pk",
            "name",
            "detail",
            "explanation",
        )


class ExperienceListSerializer(serializers.ModelSerializer):
    is_host = serializers.SerializerMethodField()
    videos = VideoSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "rating",
            "is_host",
            "country",
            "city",
            "name",
            "price",
            "address",
            "start",
            "end",
            "description",
            "videos",
        )

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_rating(self, experience):
        return experience.rating()


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_host = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    videos = VideoSerializer(
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    perks = PerkSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = "__all__"

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_rating(self, experience):
        return experience.rating()
