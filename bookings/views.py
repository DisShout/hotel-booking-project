from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

from .models import Booking
from .serializers import BookingCreateSerializer, BookingDetailSerializer
from .services import BookingService


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        return BookingDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = BookingService.create_booking(serializer.validated_data)
        except IntegrityError:
            return Response(
                {"error": "Комната уже забронирована на эти даты."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"booking_id": str(booking.id)}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        booking_id = booking.id
        BookingService.delete_booking(booking)
        return Response(
            {"status": f"Booking {booking_id} deleted"}, status=status.HTTP_200_OK
        )

    def list(self, request, *args, **kwargs):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        bookings = BookingService.get_bookings_by_room(room_id)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
