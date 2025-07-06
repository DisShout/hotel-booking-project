from rest_framework import serializers
from .models import Booking
from datetime import date


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["room", "date_start", "date_end"]

    def to_representation(self, instance):
        return {"booking_id": str(instance.id)}

    def validate(self, attrs):
        date_start = attrs.get("date_start")
        date_end = attrs.get("date_end")
        today = date.today()

        if date_start < today:
            raise serializers.ValidationError(
                {"date_start": "Дата заезда должна быть сегодня или позже."}
            )

        if date_start >= date_end:
            raise serializers.ValidationError(
                {
                    "date_start": "Дата заезда должна быть раньше даты выезда.",
                    "date_end": "Дата выезда должна быть позже даты заезда.",
                }
            )

        return attrs


class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "date_start", "date_end"]
