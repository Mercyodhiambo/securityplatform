from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

def role_required(role, redirect_url):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)
            if getattr(request.user, 'role', None) != role:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def employer_required(redirect_url='/log_in/'):
    return role_required('employer', redirect_url)


def client_required(redirect_url='/log_in/'):
    return role_required('client', redirect_url)


def applicant_required(redirect_url='/log_in/'):
    return role_required('applicant', redirect_url)