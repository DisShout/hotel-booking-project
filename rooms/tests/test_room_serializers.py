import pytest
from rooms.serializers import RoomCreateSerializer


@pytest.mark.django_db
class TestRoomCreateSerializer:
    def test_valid_data(self):
        data = {"description": "Test Room", "price": 1500}
        serializer = RoomCreateSerializer(data=data)
        assert serializer.is_valid()
        room = serializer.save()
        assert room.description == "Test Room"
        assert room.price == 1500

    def test_invalid_price_zero(self):
        data = {"description": "Invalid Room", "price": 0}
        serializer = RoomCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "price" in serializer.errors
        assert serializer.errors["price"][0] == "Цена должна быть больше 0"

    def test_invalid_price_negative(self):
        data = {"description": "Invalid Room", "price": -100}
        serializer = RoomCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "price" in serializer.errors
        assert serializer.errors["price"][0] == "Цена должна быть больше 0"
