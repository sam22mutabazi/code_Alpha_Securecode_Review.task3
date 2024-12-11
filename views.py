from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Missing input validation
        if not username or not password or not confirm_password:
            return HttpResponse("All fields are required!")

        # No strong password criteria
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        # Missing username uniqueness check
        # Vulnerable to username conflicts
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username is already taken!")

        # Create user without validation
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Missing input validation
        if not username or not password:
            return HttpResponse("Both username and password are required!")

        # Authenticate user without error handling
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # No session security
            request.session['user_id'] = user.id  # Directly store user ID in session

            return redirect('home')
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render

# Create your views here.
