from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    job_list, job_detail, register_user, log_in, home, 
    applicant, clients, our_services, about_us, 
    employer, profile, apply,   
    submit_application,  post_job,
    landing_page, add_security_agency, list_agencies, update_security_companies, log_out, profile
)

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Landing page URL
    path('home/', home, name='home'),  
    path('register_user/', register_user, name='register_user'),
    path('log_in/', log_in, name='log_in'),
    path('log_out/', log_out, name='log_out'),  
    path('applicant/', applicant, name='applicant'),
    path('clients/', clients, name='clients'),
    path('our_services/', our_services, name='our_services'),
    path('about_us/', about_us, name='about_us'),
    path('employer/', employer, name='employer'),
    path('profile/', profile, name='profile'),
    path('apply/<int:job_id>/', apply, name='apply'),
    path('submit_application/<int:job_id>/', submit_application, name='submit_application'),  
    path('jobs/', job_list, name='job_list'),
    path('jobs/new/', post_job, name='post_job'),
    path('jobs/<int:job_id>/details', job_detail, name='job_detail'),
    path('agencies/', list_agencies, name='list_agencies'), 
    path('agencies/new/', add_security_agency, name='add_security_agency'),
    path('company/update/<int:company_id>/', update_security_companies, name='update_security_companies'), 
     path('profile/', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)