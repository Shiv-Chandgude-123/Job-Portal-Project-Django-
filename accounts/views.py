from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm, CustomPasswordChangeForm
from .forms import EditProfileForm


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps user logged in
            messages.success(request, "✅ Your password was successfully updated!")
            return redirect('profile')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # redirect back to profile page
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})

def signup_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ imported above
            return redirect("job_list")  # we will create job_list later
    else:
        form = UserRegisterForm()
    return render(request, "accounts/signup.html", {"form": form})  # ✅ render is imported

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # ✅ no underline now
            return redirect("job_list")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)  # ✅ imported above
    return redirect("login")
