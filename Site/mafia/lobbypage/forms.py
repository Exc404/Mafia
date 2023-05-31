from django import forms
from .models import Rooms
from django import forms
from django.core.exceptions import ValidationError

class CreateTheRoom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    roomname = forms.CharField(max_length=40)

    def clean_roomname(self):
        rname = self.cleaned_data['roomname'].strip()
        if Rooms.objects.filter(roomname=rname).exists():
            raise ValidationError('Эта почта уже используется!')

        return rname

    class Meta:
        model = Rooms
        fields = ('roomname',)