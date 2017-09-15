from django import forms
from .models import username_regex
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
class ReadWriteForm(forms.Form):
    data = forms.CharField(label='Data:', max_length=150,required=False)
User = get_user_model()
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'username')
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('username','email', 'password', 'is_staff', 'is_active')
    def clean_password(self):
        return self.initial["password"]
class UserLogInForm(forms.Form):
    username = forms.CharField(label='Username', validators=[
        RegexValidator(
            regex=username_regex,
            message='Username must be alphanumberic containing +-*.',
            code= 'Invalid Username'
        )])
    password = forms.CharField(label='Password ', widget=forms.PasswordInput)
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        the_user = authenticate(username=username, password=password)
        if not the_user:
            raise forms.ValidationError("Invalid Credentials")
        return super(UserLogInForm, self).clean(*args,**kwargs)



# class UserLogInForm(forms.ModelForm):
#     username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),validators=[
#         RegexValidator(
#             regex=username_regex,
#             message='Username must be alphanumberic containing +-*.',
#             code= 'Invalid Username'
#         )])
#     password = forms.CharField(label='Password ', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")
#         the_user = authenticate(username=username, password=password)
#         if not the_user:
#             raise forms.ValidationError("Invalid Credentials")
#         return super(UserLogInForm, self).clean(*args,**kwargs)
#     class Meta:
#         model = User
#         fields = ['username','password']