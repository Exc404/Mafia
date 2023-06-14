from django import forms
from .models import Profile
from django import forms


class EditProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    nickname = forms.CharField(label="Новый никнейм", max_length=20)
    profile_img = forms.ImageField(label="Новое фото профиля:", required=False)

    class Meta:
        model = Profile
        fields = ('profile_img', 'nickname')


class FriendsSearchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    nickname = forms.CharField(label="Никнейм пользователя:", max_length=20)

    class Meta:
        model = Profile
        fields = ('nickname',)
