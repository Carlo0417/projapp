from django.db import models

# Create your models here.
# ROOM
# Id	room_name	floor	dorm_name	description
# 1	101		1st	male dorm	4-bed spacer
# 2	102		1st	female dorm	2-bed spacer
# 3	103		1st	male dorm	4-bed spacer

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Room(BaseModel):
    DORMNAME_CHOICES = (('Male Dorm','Male Dorm'), ('Female Dorm','Female Dorm'))
    room_name = models.CharField(max_length=25)
    floorlvl = models.CharField(max_length=25, verbose_name="Floor Level")
    dorm_name = models.CharField(max_length=25, choices=DORMNAME_CHOICES)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.room_name}"