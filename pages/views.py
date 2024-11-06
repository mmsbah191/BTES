import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# views.py
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse

from .forms import (EventForm, LoginForm, PaymentForm, ProfileImageForm,
                    RefundRequestForm, TicketForm, UserForm)
from .models import Event, User


# Create your views here.
def index(request):
    return HttpResponse("HttpResponse empty page")


def home(request):
    events = Event.objects.all()
    return render(request, "pages/home.html", {"events": events})


@login_required
def create_event(request):
    if not request.user.role == "publisher":
        return HttpResponse("not authorized you must be publisher for login")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("create_event")
        else:
            print(form.errors)
    else:
        form = EventForm()
    return render(request, "pages/create_event.html", {"form": form})


@login_required
def create_ticket(request):
    if not request.user.role == "publisher":
        return HttpResponse("not authorized you must be publisher for create_ticket")

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_ticket")
    else:
        form = TicketForm()
    return render(request, "pages/create_ticket.html", {"form": form})


@login_required
def create_refund_request(request):
    if not request.user.role == "publisher":
        return HttpResponse(
            "not authorized you must be publisher for create_refund_request"
        )
    if request.method == "POST":
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_refund_request")
    else:
        form = RefundRequestForm()
    return render(request, "pages/create_refund_request.html", {"form": form})

def signup(request):
    if request.user.is_authenticated: 
        return redirect('home')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            form.instance.username = str(email).split("@")[0]
            password = form.cleaned_data["password"]
            form.instance.password = make_password(password)  # تشفير كلمة المرور

            if User.objects.filter(email=email).exists():
                form.add_error("email", "This email is already registered.")

            # elif User.objects.filter(username=username).exists():
            #     form.add_error("username", "This username is already taken.")

        if not form.errors:
            form.save()
            return redirect("login_view")
        else:
            # If exists & fails show an error message
            return render(
                request,
                "pages/signup.html",
                {"error": "choose another username.", "form": form},
            )

    else:
        form = UserForm()
    return render(request, "pages/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        return redirect('home')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                username = User.objects.get(email=email).username
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                user = authenticate(request, username=email, password=password)

            if user is not None:
                # If user is authenticated, log them in using the built-in login function
                login(request, user)
                return redirect(
                    "home"
                )  # Redirect to a page after login (e.g., home page)
            else:
                # If authentication fails, show an error message
                return render(
                    request,
                    "pages/login.html",
                    {"form": form, "error": "Invalid username or password."},
                )
    else:
        form = LoginForm()
    return render(request, "pages/login.html", {"form": form})


@login_required
def update_profile_image(request):
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            if not request.FILES.get("profile_image"):  # If no image uploaded
                user.profile_image = "static/images/profile.png"  # Set to default image
            user.save()
            return redirect("home")
    else:
        form = ProfileImageForm(instance=request.user)
    return render(request, "pages/update_profile_image.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def create_payment(request):
    if not request.user.role == "publisher":
        return HttpResponse("not authorized you must be publisher for create_payment")
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_payment")
    else:
        form = PaymentForm()
    return render(request, "pages/create_payment.html", {"form": form})


def link_list(request):
    # جمع الروابط المتاحة
    links = [
        {"name": "AdminPanel database", "url": "admin/"},
        # {"name": "index", "url": reverse("index")},
        {"name": "Home", "url": reverse("home")},
        {"name": "Create User", "url": reverse("signup")},
        {"name": "login User", "url": reverse("login_view")},
        {"name": "Create Event", "url": reverse("create_event")},
        {"name": "Create Ticket", "url": reverse("create_ticket")},
        {"name": "Create Refund Request", "url": reverse("create_refund_request")},
        {"name": "Create Payment", "url": reverse("create_payment")},
    ]
    return render(request, "pages/link_list.html", {"links": links})
