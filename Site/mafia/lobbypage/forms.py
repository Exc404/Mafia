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
        allowed_chars = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        if Rooms.objects.filter(roomname=rname).exists():
            raise ValidationError('Это имя комнаты уже используется!')

        for char in rname:
            if char not in allowed_chars:
                raise forms.ValidationError('Недопустимый символ: {}'.format(char))

        return rname

    class Meta:
        model = Rooms
        fields = ('roomname',)