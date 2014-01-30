from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    email.widget.attrs.update({'placeholder' : 'Enter Your Email'})
    first_name.widget.attrs.update({'placeholder' : 'Enter Your First Name'})
    last_name.widget.attrs.update({'placeholder' : 'Enter Your Last Name'})

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder' : 'Choose an Username'})
        self.fields['password1'].widget.attrs.update({'placeholder' : 'Choose Password'})
        self.fields['password2'].widget.attrs.update({'placeholder' : 'Re-type Password'})


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.clean_email()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data["password2"])

        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    error_messages = {
        'invalid_login': _("Please enter a correct email and password."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                self._errors["password"] = self.error_class([self.error_messages['invalid_login']])
                raise forms.ValidationError(self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                self._errors["email"] = self.error_class([self.error_messages['inactive']])

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

