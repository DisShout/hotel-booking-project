import pytest
from rest_framework.test import APIClient
from rooms.models import Room


@pytest.mark.django_db
class TestRoomViewSet:
    def setup_method(self):
        self.client = APIClient()

    def test_create_room(self):
        data = {"description": "Стандартный номер Google", "price": 2000}
        response = self.client.post("/rooms/", data, format="json")

        assert response.status_code == 201
        assert "room_id" in response.data
        assert Room.objects.count() == 1

    def test_list_rooms(self):
        Room.objects.create(description="Номер 1", price=1000)
        Room.objects.create(description="Номер 2", price=1500)

        response = self.client.get("/rooms/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_delete_room(self):
        room = Room.objects.create(description="Удаляемый", price=1200)

        response = self.client.delete(f"/rooms/{room.id}/")
        assert response.status_code == 200
        assert Room.objects.count() == 0
