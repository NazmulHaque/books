from django import forms
from models import UserProfile

class UploadProfilePhoto(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo',)

class UserBasicInfoForm(forms.ModelForm):
    contact_number = forms.CharField(required=True)
    birthday = forms.DateField(required=True)

    class Meta:
        model = UserProfile
        exclude = ['user', 'photo']

