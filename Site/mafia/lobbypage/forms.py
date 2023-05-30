from django import forms
from .models import Rooms
from django import forms


class CreateTheRoom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    roomname = forms.CharField(max_length=40)

    class Meta:
        model = Rooms
        fields = ('roomname',)