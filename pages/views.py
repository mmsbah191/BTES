from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse

from .forms import (EventForm, PaymentForm, RefundRequestForm, TicketForm,
                    UserForm)


# Create your views here.
def index(request):
    return HttpResponse("HttpResponse empty page")




def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_event')  
        else:
            print(form.errors)  
    else:
        form = EventForm()
    return render(request, 'pages/create_event.html', {'form': form})




def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_ticket')  
    else:
        form = TicketForm()
    return render(request, 'pages/create_ticket.html', {'form': form})



def create_refund_request(request):
    if request.method == 'POST':
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_refund_request')  
    else:
        form = RefundRequestForm()
    return render(request, 'pages/create_refund_request.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_user') 
    else:
        form = UserForm()
    return render(request, 'pages/create_user.html', {'form': form})

def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_payment')  
    else:
        form = PaymentForm()
    return render(request, 'pages/create_payment.html', {'form': form})


def link_list(request):
    # جمع الروابط المتاحة
    links = [
        {"name": "Home", "url": reverse("index")},
        {"name": "Create Event", "url": reverse("create_event")},
        {"name": "Create Ticket", "url": reverse("create_ticket")},
        {"name": "Create Refund Request", "url": reverse("create_refund_request")},
        {"name": "Create User", "url": reverse("create_user")},
        {"name": "Create Payment", "url": reverse("create_payment")},
    ] 
    return render(request, "pages/link_list.html", {"links": links})