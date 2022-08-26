from django.contrib import admin

# Register your models here.
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=("room_name","floorlvl","description",)
    search_fields = ("room_name","dorm_name",)
    list_filter = ("created_at",)