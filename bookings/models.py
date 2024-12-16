from django.db import models
from common.models import CommonModel


# Create your models here.
class Booking(CommonModel):
    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        EXPERIENCES = "experiences", "Experiences"
        ROOMS = "rooms", "Rooms"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()
    not_canceled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.kind.title()} booking for: {self.user}"
