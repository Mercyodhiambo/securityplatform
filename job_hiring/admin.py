from django.contrib import admin
from .models import Applicant, Job,  SecurityCompany, User, JobApplication, Hire

admin.site.register(Applicant)  
admin.site.register(Job)  
admin.site.register(SecurityCompany)  
admin.site.register(User)  
admin.site.register(JobApplication)
admin.site.register(Hire)
