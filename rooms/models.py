from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id} — {self.price}₽"

    class Meta:
        db_table = "rooms"
