from .models import Booking


class BookingService:
    @staticmethod
    def create_booking(data: dict) -> Booking:
        return Booking.objects.create(**data)

    @staticmethod
    def delete_booking(booking: Booking) -> None:
        booking.delete()

    @staticmethod
    def get_bookings_by_room(room_id: int):
        return Booking.objects.filter(room_id=room_id).order_by("date_start")
