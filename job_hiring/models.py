from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# User model definition
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    role = models.CharField(max_length=50, choices=[
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        ('client', 'Client'),
    ])
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Required fields for creating a superuser

    def __str__(self):
        return self.username


    def __str__(self):
        return self.username

# SecurityCompany model definition
class SecurityCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure company name is unique
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)  # Optional logo field
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, default='Unknown Location')
    services_offered = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User model
    def __str__(self):
        return self.name

# Job model definition
class Job(models.Model):
    security_company = models.ForeignKey( SecurityCompany, on_delete=models.CASCADE, null=True, blank=True)  # Link to SecurityCompany model
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)  # Optional field for job requirements
    posted_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    deadline = models.DateTimeField(null=True, blank=True)  # Optional deadline field

    def __str__(self):
        return self.title

# Applicant model definition
class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User model
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Optional resume field
    
    def __str__(self):
        return self.user.first_name if self.user else "No User"  # Return user's first name or "No User" if not linked
    

# JobApplication model definition
class JobApplication(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True, blank=True)  # Link to Applicant model
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.FileField(upload_to='cover_letters/')
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE)  # Allow null values
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')

    def __str__(self):
        applicant_name = self.applicant.user.first_name if self.applicant and self.applicant.user else "No Applicant"
        job_title = self.job.title if self.job else "No Job"
        return f'{applicant_name} - {job_title}'
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    # Add other fields as needed
    
    def __str__(self):
        return self.company_name
    

class Hire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    security_company = models.ForeignKey(
        SecurityCompany, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('hired', 'Hired'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    def __str__(self):
        client_username = self.client.user.username if self.client and self.client.user else "Unknown Client"
        company_username = self.security_company if self.security_company and self.security_company.name else "Unknown Company"
        return f"{client_username} hired {company_username}"
