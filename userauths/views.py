from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("core:index")
    else:
        print("User can't register")
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign_up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.all(email=email)
        except:
            messages.warning(request, f"User with {email} does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect("core:index")
        else:
            messages.warning(request, "User Does Not Exist")

    context = {}

    return render(request, "userauths/sign_in.html", context)
