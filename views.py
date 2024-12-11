from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validate input fields
        if not username or not password or not confirm_password:
            return HttpResponse("All fields are required!")
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        # Strong password criteria
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return HttpResponse("Password must be at least 8 characters long and contain a number!")

        # Ensure unique username
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username is already taken!")

        # Validate username as email
        try:
            validate_email(username)
        except ValidationError:
            return HttpResponse("Invalid email format for username!")

        # Create user
        User.objects.create_user(username=username, password=password)
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Validate inputs
        if not username or not password:
            return HttpResponse("Both username and password are required!")

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Add session security
            request.session.set_expiry(0)  # Session expires when browser is closed
            request.session['user_id'] = user.id  # Store user ID in session

            return redirect('home')  # Redirect to home page after login
        else:
            return HttpResponse("Invalid credentials! Please try again.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout
