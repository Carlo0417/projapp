from django.forms import ModelForm

from .models import Room

from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

        

