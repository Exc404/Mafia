from django import forms
from .models import Profile
from django import forms


class ImageForm(forms.ModelForm):
    profileImg = forms.ImageField

    class Meta:
        model = Profile
        fields = ('profile_img',)


class NicknameForm(forms.ModelForm):
    nickname = forms.CharField

    class Meta:
        model = Profile
        fields = ('nickname',)
