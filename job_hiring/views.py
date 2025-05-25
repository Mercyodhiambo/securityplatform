from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required  # Import the decorator
from .models import Job, SecurityCompany, Applicant, JobApplication, User, Client
 # Import your models
from django.shortcuts import redirect
from .forms import UserForm , UserUpdateForm , ProfileUpdateForm 
from .models import Profile 



# View for listing all jobs
def job_list(request):
    jobs = Job.objects.all()  # Fetch all job entries
    return render(request, 'jobs.html', {'jobs': jobs}) 

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
def profile(request):  
    return render(request, 'profile.html')

# View for user registration
def register_user(request):
    return sign_up(request)  # Just call the sign_up function

# View for job details
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_details.html', {'job': job})

# View for sign-up
def sign_up(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        form = UserForm(request.POST)
        if form.is_valid():
           user = form.save()
           if role == 'applicant':
                # Create an Applicant instance if the user is an applicant
                applicant = Applicant.objects.create(user=user)
                applicant.save()
                # Automatically log in the user after registration
                login(request, user)
                messages.success(request, 'Applicant account created successfully!')
                return redirect('home')
        print(f"Form errors: {form.errors}")  
        if role == 'employer':
            # Create a SecurityCompany instance if the user is an employer
            company = SecurityCompany.objects.create(user=user)
            company.save()
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, 'Employer account created successfully!')
            return redirect('home')
        elif role == 'client':
            # Create a Client instance if the user is a client
            client = Client.objects.create(user=user)
            client.save()
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, 'Client account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error creating account. Please check the form.')
            return redirect('sign_up')
    return render(request, 'sign_up.html', {'page': 'sign_up'})


def landing_page(request):
    return render(request, 'landing_page.html', {'page': 'landing'})

# View for login
def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('log_in')
   

    return render(request, 'log_in.html')

def log_out(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('landing_page')  # Redirect to the landing page or any other page

   
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


# View for posting a job
def post_job(request):
    # Assuming you have a way to check the user's role
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        employer_id = request.user.id  # Use the user's ID

        

    return render(request, 'post_job.html')

def list_agencies(request):
    agencies = SecurityCompany.objects.all()  # Fetch all employers/agencies
    return render(request, 'list_agencies.html', {'agencies': agencies})

def add_security_agency(request):
    return render(request, 'new_security_agency.html') 

def update_security_companies(request, company_id):
    company = get_object_or_404(SecurityCompany, id=company_id)

    if request.method == 'POST':
        company.description = request.POST.get('description', company.description)
        company.location = request.POST.get('location', company.location)
        company.services_offered = request.POST.get('services_offered', company.services_offered)  
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

@login_required
def profile(request):
    if request.method == 'POST':
        # Update forms with POST data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        # Initialize forms with current user data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'profile.html', context)

