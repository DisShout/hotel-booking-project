from .models import Room

ALLOWED_SORT_FIELDS = ["price", "created_at"]


class InvalidSortFieldError(Exception):
    pass


class RoomService:
    @staticmethod
    def create_room(data: dict) -> Room:
        return Room.objects.create(**data)

    @staticmethod
    def delete_room(room: Room) -> None:
        room.delete()

    @staticmethod
    def get_sorted_rooms(sort_field: str, order: str) -> list[Room]:
        if sort_field not in ALLOWED_SORT_FIELDS:
            raise InvalidSortFieldError("Invalid sort field")

        ordering = sort_field if order == "asc" else f"-{sort_field}"
        return Room.objects.all().order_by(ordering)
