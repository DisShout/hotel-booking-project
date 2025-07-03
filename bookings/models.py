from django.db import models
from django.contrib.postgres.fields import DateRangeField
from django.contrib.postgres.constraints import ExclusionConstraint
from django.db.models import F
import uuid
from psycopg2.extras import DateRange
from rooms.models import Room


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    date_range = DateRangeField(null=True, blank=True)

    class Meta:
        db_table = "bookings"
        constraints = [
            ExclusionConstraint(
                name="prevent_overlapping_bookings",
                expressions=[
                    (F("room"), "="),
                    ("date_range", "&&"),
                ],
            ),
        ]

    def save(self, *args, **kwargs):
        self.date_range = DateRange(self.date_start, self.date_end, "[)")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking room {self.room.id}. start: {self.date_start}, end: {self.date_end}"
