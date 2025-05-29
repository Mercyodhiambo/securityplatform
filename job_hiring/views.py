from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required  # Import the decorator
from .models import Job, SecurityCompany, Applicant, JobApplication, User, Client
# Import your models
from django.shortcuts import redirect
from .forms import CustomUserForm, ApplicantForm, SecurityCompanyForm, ClientForm, JobForm, JobApplicationForm, HireForm
from .models import User, Applicant, SecurityCompany, Client, Hire
from .decorators import employer_required, client_required, applicant_required


def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            role = user_form.cleaned_data.get('role')

            if role == 'applicant':
                applicant_form = ApplicantForm(request.POST, request.FILES)
                if applicant_form.is_valid():
                    applicant = applicant_form.save(commit=False)
                    applicant.user = user
                    applicant.save()

            elif role == 'employer':
                company_form = SecurityCompanyForm(request.POST, request.FILES)
                if company_form.is_valid():
                    company = company_form.save(commit=False)
                    company.user = user
                    company.save()

            elif role == 'client':
                client_form = ClientForm(request.POST)
                if client_form.is_valid():
                    client = client_form.save(commit=False)
                    client.user = user
                    client.save()

            login(request, user)
            messages.success(
                request, 'Registration successful! You are now logged in.')
            # Redirect to the landing page or any other page
            return redirect('landing_page')
        else:
            messages.error(
                request, 'Registration failed. Please correct the errors below.')
            applicant_form = ApplicantForm()
            company_form = SecurityCompanyForm()
            client_form = ClientForm()
            # If the form is not valid, re-render the form with errors
            # print errors
            print(user_form.errors)
            print(applicant_form.errors)
            print(company_form.errors)
            print(client_form.errors)
            return render(request, 'register.html', {
                'user_form': user_form,
                'applicant_form': applicant_form,
                'company_form': company_form,
                'client_form': client_form
            })
    else:
        user_form = CustomUserForm()
        applicant_form = ApplicantForm()
        company_form = SecurityCompanyForm()
        client_form = ClientForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'applicant_form': applicant_form,
        'company_form': company_form,
        'client_form': client_form
    })


def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('landing_page')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('log_in')

    return render(request, 'log_in.html')


def log_out(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    # Redirect to the landing page or any other page
    return redirect('landing_page')


@login_required
def profile(request):
    user = request.user
    context = {}

    if user.role == 'applicant':
        applications = JobApplication.objects.filter(applicant=user.applicant)
        total_applications = applications.count()
        accepted = applications.filter(status='accepted').count()
        rejected = applications.filter(status='rejected').count()
        pending = applications.filter(status='pending').count()
        context.update({
            'applications': applications,
            'total_applications': total_applications,
            'accepted': accepted,
            'rejected': rejected,
            'pending': pending,
            'role': 'applicant',
        })

    elif user.role == 'client':
        hires = user.client.hire_set.all()
        total_hires = hires.count()
        completed = hires.filter(status='completed').count()
        ongoing = hires.filter(status='hired').count()
        security_agencies_count = SecurityCompany.objects.count()
        context.update({
            'hires': hires,
            'total_hires': total_hires,
            'completed': completed,
            'ongoing': ongoing,
            'security_agencies_count': security_agencies_count,
            'role': 'client',
        })

    elif user.role == 'employer':
        company = user.securitycompany
        jobs = Job.objects.filter(security_company=company)
        total_jobs = jobs.count()
        total_applications = JobApplication.objects.filter(job__in=jobs).count()
        # Show hires where this company was selected by clients
        hires = Hire.objects.filter(security_company=company)
        print(f"Hires for company {company.name}: {hires}")  # Debugging line
        total_hires = hires.count()
        completed = hires.filter(status='completed').count()
        ongoing = hires.filter(status='hired').count()
        context.update({
            'jobs': jobs,
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'employer_hires': hires,
            'total_hires': total_hires,
            'completed': completed,
            'ongoing': ongoing,
            'role': 'employer',
        })

    return render(request, 'profile.html', context)



def job_list(request):
    jobs = Job.objects.all().order_by('-posted_date')
    return render(request, 'jobs.html', {'jobs': jobs})



@employer_required()
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.security_company = request.user.securitycompany  # Assuming employer is linked
            job.save()
            return redirect('job_list')  # name of job listing view
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = JobApplication.objects.filter(job_id=job_id)
    return render(request, 'job_details.html', {'job': job, 'applications': applications})


@applicant_required()
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicant = request.user.applicant

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = applicant
            application.job = job
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            # If the form is not valid, re-render the form with errors
            print(form.errors)
            return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})
    else:
        # If the request is GET, initialize an empty form
        form = JobApplicationForm()

    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@client_required()
def hire_agency(request, agency_id):
    firm = SecurityCompany.objects.get(id=agency_id)
    client = request.user.client
    print(f"Client: {client}, Security Company: {firm}")  # Debugging line

    if request.method == 'POST':
        form = HireForm(request.POST)
        if form.is_valid():
            hire = form.save(commit=False)
            hire.client = client
            hire.security_company = firm
            hire.save()
            return redirect('profile')
    else:
        form = HireForm(initial={'security_company': firm})

    return render(request, 'hire_firm.html', {'form': form, 'firm': firm})

# View for clients page
def clients(request):
    return render(request, 'clients.html')

# View for our services page


def our_services(request):
    return render(request, 'our_services.html')

# View for about us page


def about_us(request):
    return render(request, 'about_us.html', {'page': 'about_us'})

# View for employer page


def employer(request):
    return render(request, 'employer.html')

# View for profile page



# View for job details


def landing_page(request):
    return render(request, 'landing_page.html', {'page': 'landing'})


# View for home
def home(request):
    return render(request, 'home.html')

# View for applicant page


def applicant(request):
    return render(request, 'applicant.html')

# View for applying to a job


def apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    print(f"Job ID: {job.id}, Job Title: {job.title}")  # Debugging line
    return render(request, 'apply.html', {'job': job})

# View for submitting an application


def submit_application(request, job_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume = request.FILES.get('resume')
        cover_letter = request.FILES.get('cover_letter')

    return render(request, 'apply.html', {'job_id': job_id})



def list_agencies(request):
    agencies = SecurityCompany.objects.all()  # Fetch all employers/agencies
    return render(request, 'list_agencies.html', {'agencies': agencies})


def add_security_agency(request):
    return render(request, 'new_security_agency.html')


def update_security_companies(request, company_id):
    company = get_object_or_404(SecurityCompany, id=company_id)

    if request.method == 'POST':
        company.description = request.POST.get(
            'description', company.description)
        company.location = request.POST.get('location', company.location)
        company.services_offered = request.POST.get(
            'services_offered', company.services_offered)
        company.save()
        messages.success(request, 'Company details updated successfully!')
        return redirect('list_agencies')  # Adjust as necessary

    return render(request, 'update_security_company.html', {'company': company})


def submit_application(request, job_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume = request.FILES.get('resume')
        cover_letter = request.FILES.get('cover_letter')

    return render(request, 'apply.html', {'job_id': job_id})



