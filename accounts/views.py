from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.urls import reverse

from .forms import UserRegisterForm



def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Not saved to DB yet
            user.email = form.cleaned_data.get('username')
            user.is_active = False  # Set inactive
            user.save()  # Now save to DB

            # Proceed with email sending...
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"http://{current_site.domain}{activation_link}"

            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'activation_url': activation_url,
            })
            to_email = form.cleaned_data.get('username')
            email = EmailMessage('Activate your account', message, to=[to_email])
            try:
                email.send()
                print("Activation email sent to", to_email)
            except Exception as e:
                print("Email sending failed:", e)


            messages.success(request, 'Please confirm your email address to complete registration.')
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # <- Add this for debugging
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('register')



# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # You can change to dashboard or any page
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

@login_required
def home_view(request):
    messages.success(request, f"Welcome {request.user.username}, you have successfully logged in!")
    return render(request, 'accounts/home.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Password Reset View
def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Password Reset Request"
                    email_template = render_to_string("accounts/password_reset_email.html", {
                        "email": user.email,
                        "domain": request.META['HTTP_HOST'],
                        "site_name": "Your Site",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    })
                    send_mail(subject, email_template, None, [user.email])
            messages.success(request, "If that email exists, we've sent a password reset link.")
            return redirect("login")
    else:
        form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {"form": form})
