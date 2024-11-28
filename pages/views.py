import os
from time import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse

from pages import models

from .forms import (EventForm, LoginForm, PaymentForm, ProfileImageForm,
                    RefundRequestForm, TicketForm, UserForm)
from .models import Cart, Event, Payment, Ticket, User


# Create your views here.
def index(request):
    return redirect(link_list)


def home(request):
    events = Event.objects.all()
    if str(request.user) != "AnonymousUser" and request.user.role == "publisher":
        return render(request, "pages/home_delete.html", {"events": events})
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


def create_ticket(request):
    if str(request.user) != "AnonymousUser" and not request.user.role == "publisher":
        return HttpResponse("not authorized you must be publisher for create_ticket")

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_ticket")
    else:
        form = TicketForm()
    return render(request, "pages/create_ticket.html", {"form": form})


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "pages/event_details.html", {"event": event})


def create_refund_request(request):
    if str(request.user) != "AnonymousUser" and request.user.role == "publisher":
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
        return redirect("home")
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
                {"error": "error", "form": form},
            )

    else:
        form = UserForm()
    return render(request, "pages/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        return redirect("home")

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
                    {"form": form, "error": "error"},
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
                user.profile_image = "images/profile.png"  # Set to default image
            user.save()
            return redirect("home")
    else:
        form = ProfileImageForm(instance=request.user)
    return render(request, "pages/update_profile_image.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required  # regular user only can make direct payment
def create_payment(request):
    if request.user.role == "publisher":
        return HttpResponse("not authorized you must be publisher for create_payment")
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_payment")
    else:
        form = PaymentForm()
    return render(request, "pages/create_payment.html", {"form": form})


@login_required
def checkout_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.amount = event.price
            payment.payment_status = "pending"
            payment.save()
            return redirect("payment_confirmation", event_id=event_id)
            return redirect("payment_confirmation", payment_id=payment.id)
    else:
        form = PaymentForm()
    return render(request, "pages/checkout_event.html", {"event": event, "form": form})




@login_required
def payment_confirmation(request, event_id):
    try:
        # الحصول على الدفع بناءً على ID
        event = get_object_or_404(Event, id=event_id)

        if request.method == "POST":
            # if payment.payment_status == "pending":
            #     payment.payment_status = "completed"
            #     payment.save()

                try:
                    # إنشاء التذكرة وربطها بالمستخدم والحدث
                    ticket = Ticket(
                        event=event,
                        user=request.user,
                    )  # الكمية المطلوب
                    # محاولة شراء التذكرة وتحديث التوافر
                    ticket.purchase_ticket()
                    ticket.save()
                except ValueError as e:
                    return HttpResponse(f"Unexpected Error: {str(e)}", status=500)
        return redirect("booked_events")
    # except Payment.DoesNotExist:
    #                     return HttpResponse(f"Error: {str(e)}", status=400)
    except Exception as e:
        return HttpResponse(f"Unexpected Error: {str(e)}", status=500)


@login_required  # regular user only can make direct payment
def checkout_card(request):
    if str(request.user) != "AnonymousUser" and request.user.role == "publisher":
        return HttpResponse(
            "Not authorized. You must be a publisher to create payment."
        )
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("payment_confirmation")
    else:
        form = PaymentForm(initial={"cart": cart})
    return render(request, "pages/checkout_event.html", {"form": form, "cart": cart})


@login_required
def booking(request):  # checkout
    cart = Cart.objects.get()
    return render(request, "cart/checkout.html", {"cart": cart})


@login_required
def add_to_cart(request, event_id):  # Use event_id instead of ticket_id
    if request.method == "POST" and request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)  # Fetch by event_id
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.add(event)
        cart.save()
    return redirect("home")


def delete_from_cart(request, event_id):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        event = get_object_or_404(Event, id=event_id)
        cart.items.remove(event)  # احذف العنصر من السلة
        cart.save()
    return redirect("view_cart")


@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, "pages/view_cart.html", {"cart": cart})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "DELETE":
        event.delete()
    return redirect("home")


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EventForm(instance=event)
    return render(request, "pages/edit_event.html", {"form": form})


# def link_list(request):
#     return render(request, "pages/edit_event.html", {"form": form})


def link_list(request):
    # جمع الروابط المتاحة
    links = [
        {"name": "AdminPanel database", "url": "admin/"},
        # {"name": "index", "url": reverse("index")},
        {"name": "Home", "url": reverse("home")},
        {"name": "Create User", "url": reverse("signup")},
        {"name": "login User", "url": reverse("login_view")},
        {"name": "view cart", "url": reverse("view_cart")},
        {"name": "Create Event", "url": reverse("create_event")},
        {"name": "Create Ticket", "url": reverse("create_ticket")},
        {"name": "Create Refund Request", "url": reverse("create_refund_request")},
    ]
    return render(request, "pages/link_list.html", {"links": links})


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render


def search_event(request):
    query = request.GET.get("q", "")  # جلب من html
    query = query.strip()  # تأكد من إزالة الفراغات من البداية والنهاية
    results = Event.objects.none()  # تهيئة النتائج فارغ

    if query:
        # البحث باستخدام شروط متعددة
        results = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()  # `distinct` لتجنب التكرار في النتائج

    return render(
        request, "pages/search_event.html", {"query": query, "events": results}
    )


@login_required
def booked_events(request):
    # جلب الحجوزات الخاصة بالمستخدم
    user_Tickets = Ticket.objects.filter(user=request.user)
    return render(request, "pages/booked_events.html", {"tickets": user_Tickets})


@login_required
def delete_booking(request, booking_id):
    # حذف حجز معين
    booking = get_object_or_404(booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect("booked_events")  # إعادة التوجيه إلى صفحة الحجوزات
