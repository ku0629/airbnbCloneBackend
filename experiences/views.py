from django.db import transaction
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Perk, Experience
from categories.models import Category
from .serializers import (
    PerkSerializer,
    ExperienceListSerializer,
    ExperienceDetailSerializer,
)
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer, VideoSerializer
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperienceBookingSerializer,
)
from medias.models import Video
from bookings.models import Booking

# Create your views here.


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            serializer = PerkSerializer(new_perk)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            perk = Perk.objects.get(pk=pk)
            return perk
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serialzer = PerkSerializer(perk, data=request.data, partial=True)
        if serialzer.is_valid():
            updated_perk = serialzer.save()
            serialzer = PerkSerializer(updated_perk)
            return Response(serialzer.data)
        else:
            return Response(serialzer.erorrs)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceListSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'experiences'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    new_experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        new_experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise ParseError("Perk not found")
            except Exception as e:
                raise ParseError(e)
            serializer = ExperienceDetailSerializer(
                new_experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be experiences")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found")
            try:
                with transaction.atomic():
                    if category_pk:
                        updated_experience = serializer.save(
                            category=category,
                        )
                    else:
                        updated_experience = serializer.save()
                    perks_list = request.data.get("perks")
                    if perks_list:
                        updated_experience.perks.clear()
                        for perk_pk in perks_list:
                            perk = Perk.objects.get(pk=perk_pk)
                            updated_experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise ParseError("Perk not found")
            except Exception as e:
                raise ParseError(e)
            serializer = ExperienceDetailSerializer(
                updated_experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        experience = self.get_object(pk)
        perks = experience.perks.all()[start:end]
        serializer = PerkSerializer(
            perks,
            many=True,
        )
        return Response(serializer.data)


class ExperienceReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        reviews = experience.reviews.all()[start:end]
        serializer = ReviewSerializer(
            reviews,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            new_review = serializer.save(
                user=request.user,
                experience=experience,
            )
            serializer = ReviewSerializer(new_review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperiencePhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(
                experience=experience,
            )
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceVideo(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        try:
            video = Video.objects.get(experience=experience)
            raise ParseError("Only one video is allowed")
        except Video.DoesNotExist:
            serializer = VideoSerializer(data=request.data)
            if serializer.is_valid():
                video = serializer.save(experience=experience)
                serializer = VideoSerializer(video)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now())

        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCES,
            experience_time__gte=now,
        )[start:end]

        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)

        if serializer.is_valid():
            new_booking = serialzier.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCES,
            )
            serialzier = PublicBookingSerializer(new_booking)
            return Response(serialzier.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):
    def get_experience(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise NotFound

    def get_booking(self, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            return booking
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        experience = self.get_experience(pk)
        try:
            booking = Booking.objects.get(
                experience=experience,
                pk=booking_pk,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return NotFound

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user.pk != request.user.pk:
            raise PermissionDenied
        serializer = CreateExperienceBookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_booking = serializer.save()
            serialzier = PublicBookingSerializer(updated_booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user.pk != request.user.pk:
            raise PermissionDenied
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)
