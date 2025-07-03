import pytest
from bookings.serializers import BookingCreateSerializer
from rooms.models import Room
from datetime import date, timedelta


@pytest.mark.django_db
class TestBookingCreateSerializer:
    def setup_method(self):
        self.room = Room.objects.create(description="Test Room", price=1000)

    def test_valid_dates(self):
        data = {
            "room": self.room.id,
            "date_start": date.today() + timedelta(days=1),
            "date_end": date.today() + timedelta(days=2),
        }
        serializer = BookingCreateSerializer(data=data)
        assert serializer.is_valid()

    def test_start_date_in_past(self):
        data = {
            "room": self.room.id,
            "date_start": date.today() - timedelta(days=1),
            "date_end": date.today() + timedelta(days=2),
        }
        serializer = BookingCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "date_start" in serializer.errors
        assert (
            serializer.errors["date_start"][0]
            == "Дата заезда должна быть сегодня или позже."
        )

    def test_start_date_after_end_date(self):
        data = {
            "room": self.room.id,
            "date_start": date.today() + timedelta(days=5),
            "date_end": date.today() + timedelta(days=2),
        }
        serializer = BookingCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "date_start" in serializer.errors
        assert "date_end" in serializer.errors
