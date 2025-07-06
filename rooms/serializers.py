from rest_framework import serializers
from .models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["description", "price"]

    def to_representation(self, instance):
        return {"room_id": instance.id}

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0")
        return value


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at"]
        read_only_fields = ["id", "created_at"]
