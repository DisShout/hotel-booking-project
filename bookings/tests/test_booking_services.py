import pytest
from bookings.services import BookingService
from rooms.models import Room
from datetime import date, timedelta
from django.db import IntegrityError
import psycopg2


@pytest.mark.django_db
class TestBookingService:
    def setup_method(self):
        self.room = Room.objects.create(description="Test Room", price=1000)

    def test_create_booking_success(self):
        start_date = date.today() + timedelta(days=5)
        end_date = start_date + timedelta(days=5)

        data = {
            "room": self.room,
            "date_start": start_date,
            "date_end": end_date,
        }
        booking = BookingService.create_booking(data)
        assert booking.id is not None
        assert booking.room == self.room

    def test_create_booking_conflict_raises_integrity_error(self):
        start_date = date.today() + timedelta(days=5)
        end_date = start_date + timedelta(days=5)

        data1 = {
            "room": self.room,
            "date_start": start_date,
            "date_end": end_date,
        }
        data2 = {
            "room": self.room,
            "date_start": start_date + timedelta(days=2),
            "date_end": end_date + timedelta(days=5),
        }

        BookingService.create_booking(data1)

        with pytest.raises(IntegrityError) as exc_info:
            BookingService.create_booking(data2)

        assert isinstance(exc_info.value.__cause__, psycopg2.errors.ExclusionViolation)
        assert "prevent_overlapping_bookings" in str(exc_info.value.__cause__)

    def test_create_two_adjacent_bookings(self):
        start_date1 = date.today() + timedelta(days=5)
        end_date1 = start_date1 + timedelta(days=2)

        start_date2 = end_date1  # начинается в день выезда первой брони
        end_date2 = start_date2 + timedelta(days=3)

        data1 = {
            "room": self.room,
            "date_start": start_date1,
            "date_end": end_date1,
        }
        data2 = {
            "room": self.room,
            "date_start": start_date2,
            "date_end": end_date2,
        }

        booking1 = BookingService.create_booking(data1)
        booking2 = BookingService.create_booking(data2)

        assert booking1.id is not None
        assert booking2.id is not None
