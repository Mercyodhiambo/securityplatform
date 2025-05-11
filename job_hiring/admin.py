from django.contrib import admin
from .models import Applicant, Job,  SecurityCompany, User, JobApplication 

admin.site.register(Applicant)  
admin.site.register(Job)  
admin.site.register(SecurityCompany)  
admin.site.register(User)  
admin.site.register(JobApplication)