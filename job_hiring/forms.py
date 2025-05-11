
from django import forms
from django.contrib.auth.forms import UserCreationForm
from.models import User, Profile, SecurityCompany, Job, Applicant, JobApplication
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1' ,'password2' , 'first_name', 'last_name' , 'role']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class SecurityCompanyForm(forms.ModelForm):
    class Meta:
        model = SecurityCompany
        fields = ['name', 'logo', 'description', 'location', 'services_offered']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'services_offered': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }