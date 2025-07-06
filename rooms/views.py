from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Room
from .serializers import RoomCreateSerializer, RoomDetailSerializer
from .services import RoomService, InvalidSortFieldError


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RoomCreateSerializer
        return RoomDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = RoomService.create_room(serializer.validated_data)
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        room = self.get_object()
        room_id = room.id
        RoomService.delete_room(room)
        return Response(
            {"status": f"Room {room_id} deleted"}, status=status.HTTP_200_OK
        )

    def list(self, request, *args, **kwargs):
        sort_field = request.query_params.get("sort", "created_at")
        order = request.query_params.get("order", "asc")

        try:
            rooms = RoomService.get_sorted_rooms(sort_field, order)
        except InvalidSortFieldError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
