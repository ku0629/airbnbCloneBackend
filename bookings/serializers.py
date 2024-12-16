from django.utils import timezone

from rest_framework import serializers

from .models import Booking

from users.serializers import TinyUserSerializer
from rooms.serializers import TinyRoomSerializer


# Serializer for creating room's bookings
class CreateRoomBookingSerializer(serializers.ModelSerializer):
    # 원래 Booking의 모델을 Overriding을 한다. 둘 다 디폴트로 Required = True
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    # serializer.is_valid()에서 이 검사도 같이 해준다. value는 검사하고 싶은 값을 의미
    # 여기서 valid 하면 그대로 return 아니면 raise serializers.ValidationError("error")
    def validate_check_in(self, value):
        now = timezone.localdate(timezone.now())
        if value < now:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate_check_out(self, value):
        now = timezone.localdate(timezone.now())
        if value < now:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    # 위의 메소드와 달리 이건 모든 필드의 데이터를 받아서 검사한다. data는 모든 값이 저장된 Dic이다.
    def validate(self, data):
        room = self.context.get("room")
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out!",
            )
        if Booking.objects.filter(
            room=room,
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken.",
            )
        return data


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if value < now:
            raise serializers.ValidationError("Can't book in the past!")
        return value


# Serializer for displaying room's bookings
class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class CheckMyBookingSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()
    room = TinyRoomSerializer()

    class Meta:
        model = Booking
        fields = (
            "user",
            "id",
            "room",
            "kind",
            "check_in",
            "check_out",
            "guests",
            "not_canceled",
        )
