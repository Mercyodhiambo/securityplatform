
from .models import User, Applicant, SecurityCompany, Client
from django import forms
from django.contrib.auth.forms import UserCreationForm
from.models import User, Profile, SecurityCompany, Job, Applicant, JobApplication


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role', 'password1', 'password2')


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'multiple': False, 'accept': '.pdf,.doc,.docx', 'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
        }


class SecurityCompanyForm(forms.ModelForm):
    class Meta:
        model = SecurityCompany
        fields = ['name', 'logo', 'description',
                  'location', 'services_offered']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
            'services_offered': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'address', 'phone']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-200 bg-white text-dark-gray focus:outline-none focus:border-dark-gray'}),
        }
