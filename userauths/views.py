from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.forms import UserRegisterForm, ProfileForm
from userauths.models import User, Profile

# User = settings.AUTH_USER_MODEL


# Create your views here.
def register_view(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            email = form.cleaned_data.get("email")
            messages.success(request, f"Account created for {email}!")
            new_user = authenticate(
                request,
                username=form.cleaned_data["email"],  # use email to authenticate
                password=form.cleaned_data["password1"],
            )
            if new_user is not None:  # check if authentication was successful
                login(request, new_user)
                return redirect("core:index")
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "User can't register")
            form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign_up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email")  # peanuts@gmail.com
        password = request.POST.get("password")  # getmepeanuts

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "User Does Not Exist, create an account.")

        except:
            messages.warning(request, f"User with {email} does not exist")

    return render(request, "userauths/sign_in.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect("userauths:sign-in")


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile_edit.html", context)
