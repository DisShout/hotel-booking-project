import pytest
from rest_framework.test import APIClient
from rooms.models import Room
from bookings.models import Booking
from datetime import date, timedelta
from django.db import transaction


@pytest.mark.django_db
class TestBookingViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.room = Room.objects.create(description="Test Room", price=1000)

    def test_create_booking_success(self):
        start_date = date.today() + timedelta(days=5)
        end_date = start_date + timedelta(days=5)

        data = {
            "room": self.room.id,
            "date_start": start_date.isoformat(),
            "date_end": end_date.isoformat(),
        }

        response = self.client.post("/bookings/", data, format="json")

        assert response.status_code == 201
        assert "booking_id" in response.data
        assert Booking.objects.count() == 1

    def test_create_booking_conflict_returns_400(self):
        start_date = date.today() + timedelta(days=5)
        end_date = start_date + timedelta(days=5)

        Booking.objects.create(room=self.room, date_start=start_date, date_end=end_date)

        conflict_start = start_date + timedelta(days=2)
        conflict_end = end_date + timedelta(days=5)

        data = {
            "room": self.room.id,
            "date_start": conflict_start.isoformat(),
            "date_end": conflict_end.isoformat(),
        }

        with transaction.atomic():
            response = self.client.post("/bookings/", data, format="json")
            assert response.status_code == 400
            assert "error" in response.data
            assert "забронирована" in response.data["error"]

            transaction.set_rollback(True)  # явный rollback для завершения atomic блока

        assert Booking.objects.count() == 1

    def test_list_bookings(self):
        date1_start = date.today() + timedelta(days=5)
        date1_end = date1_start + timedelta(days=2)

        date2_start = date.today() + timedelta(days=10)
        date2_end = date2_start + timedelta(days=5)

        Booking.objects.create(
            room=self.room, date_start=date1_start, date_end=date1_end
        )
        Booking.objects.create(
            room=self.room, date_start=date2_start, date_end=date2_end
        )

        response = self.client.get(f"/bookings/?room_id={self.room.id}")

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["date_start"] == date1_start.isoformat()
        assert response.data[1]["date_start"] == date2_start.isoformat()

    def test_delete_booking(self):
        start_date = date.today() + timedelta(days=5)
        end_date = start_date + timedelta(days=2)

        booking = Booking.objects.create(
            room=self.room, date_start=start_date, date_end=end_date
        )

        response = self.client.delete(f"/bookings/{booking.id}/")

        assert response.status_code == 200
        assert Booking.objects.count() == 0
