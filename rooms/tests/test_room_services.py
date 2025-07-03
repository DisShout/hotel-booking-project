import pytest
from rooms.models import Room
from rooms.services import RoomService, InvalidSortFieldError


@pytest.mark.django_db
class TestRoomService:
    def test_create_room(self):
        data = {"description": "Test Room", "price": 1000}
        room = RoomService.create_room(data)

        assert room.id is not None
        assert room.description == "Test Room"
        assert room.price == 1000

    def test_delete_room(self):
        room = Room.objects.create(description="Test Delete Room", price=1500)
        RoomService.delete_room(room)

        assert Room.objects.count() == 0

    def test_get_sorted_rooms(self):
        Room.objects.create(description="Room 1", price=1000)
        Room.objects.create(description="Room 2", price=2000)

        rooms = RoomService.get_sorted_rooms("price", "asc")
        assert rooms[0].price == 1000
        assert rooms[1].price == 2000

        rooms_desc = RoomService.get_sorted_rooms("price", "desc")
        assert rooms_desc[0].price == 2000
        assert rooms_desc[1].price == 1000

    def test_get_sorted_rooms_invalid_field(self):
        with pytest.raises(InvalidSortFieldError) as exc_info:
            RoomService.get_sorted_rooms("invalid", "asc")
        assert "Invalid sort field" in str(exc_info.value)
