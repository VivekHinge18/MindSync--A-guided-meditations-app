from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import MeditationSession, GuidedMeditation, MeditationLog, UserProfile
from .forms import MeditationSessionForm, ProfileUpdateForm

# Home Page
@login_required(login_url='/login/')
def home(request):
    if request.user.is_authenticated:
        past_sessions = MeditationSession.objects.filter(user=request.user).order_by('-session_date')
    else:
        past_sessions = None

    return render(request, 'meditation_app/home.html', {'past_sessions': past_sessions})


# List of Meditation Sessions
@login_required
def session_list(request):
    sessions = MeditationSession.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "meditation_app/session_list.html", {"sessions": sessions})

# Create a Meditation Session
@login_required
def session_create(request):
    if request.method == "POST":
        form = MeditationSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, "Meditation session added successfully!")
            return redirect("session_list")
    else:
        form = MeditationSessionForm()
    
    return render(request, "meditation_app/session_form.html", {"form": form})

# Update a Meditation Session
@login_required
def session_update(request, pk):
    session = get_object_or_404(MeditationSession, pk=pk, user=request.user)
    if request.method == "POST":
        form = MeditationSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Meditation session updated successfully!")
            return redirect("session_list")
    else:
        form = MeditationSessionForm(instance=session)
    
    return render(request, "meditation_app/session_form.html", {"form": form})

# Delete a Meditation Session
@login_required
def session_delete(request, pk):
    session = get_object_or_404(MeditationSession, pk=pk, user=request.user)
    if request.method == "POST":
        session.delete()
        messages.success(request, "Meditation session deleted successfully!")
        return redirect("session_list")
    
    return render(request, "meditation_app/session_confirm_delete.html", {"session": session})

# User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Error creating account. Please check your details.")
    else:
        form = UserCreationForm()
    
    return render(request, "meditation_app/register.html", {"form": form})

# User Login
def user_login(request):
    form = AuthenticationForm(request, data=request.POST if request.method == "POST" else None)
    
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        
        return render(request, "meditation_app/login.html", {"form": form, "login_error": "Invalid username or password!"})

    return render(request, "meditation_app/login.html", {"form": form})

# User Logout
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("home")

# List of Guided Meditations
@login_required
def guided_meditation_list(request):
    meditations = GuidedMeditation.objects.all()
    return render(request, "meditation_app/guided_meditation_list.html", {"meditations": meditations})

# Guided Meditation Details
@login_required
def guided_meditation_detail(request, pk):
    meditation = get_object_or_404(GuidedMeditation, pk=pk)
    return render(request, "meditation_app/guided_meditation_detail.html", {"meditation": meditation})

# Save Meditation Log
@login_required
def save_meditation_session(request):
    if request.method == "POST":
        meditation_type = request.POST.get("meditation_type")
        duration = request.POST.get("duration")

        if not duration.isdigit():
            messages.error(request, "Duration must be a number!")
            return redirect("home")

        MeditationLog.objects.create(user=request.user, meditation_type=meditation_type, duration=int(duration))
        messages.success(request, "Meditation session saved successfully!")
        return redirect("home")

    return render(request, "meditation_app/save_meditation.html")

# Add New Meditation Session
@login_required
def add_session(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        duration = request.POST.get("duration")

        if not duration.isdigit():
            messages.error(request, "Duration must be a number!")
            return redirect("add_session")

        MeditationSession.objects.create(user=request.user, title=title, description=description, duration=int(duration))
        messages.success(request, "Meditation session added successfully!")
        return redirect("home")

    return render(request, "meditation_app/add_session.html")

# Profile Page
@login_required
def profile_page(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect("profile")
            user.username = username

        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use!")
                return redirect("profile")
            user.email = email

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()

        if profile_form.is_valid():
            profile_form.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    profile_form = ProfileUpdateForm(instance=profile)
    return render(request, "meditation_app/profile.html", {"profile_form": profile_form})

# Delete Account
@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("register")
    
    return render(request, "meditation_app/delete_account.html")
