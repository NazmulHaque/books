from django import forms
from models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_photo',)

class UserBasicInfoForm(forms.ModelForm):
    gender = forms.ChoiceField(widget=forms.RadioSelect(),
                 choices=UserProfile.GENDER_CHOICES)
    contact_address = forms.CharField (widget=forms.widgets.Textarea(), required=False)

    class Meta:
        model = UserProfile
        exclude = ['user', 'profile_photo']

