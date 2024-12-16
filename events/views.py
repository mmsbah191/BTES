from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from pages.models import Event, Ticket

from .forms import TicketReservationForm

# views.py



def event_list(request):
    """عرض جميع الأحداث"""
    events = Event.objects.all()
    query = request.GET.get('q')
    if query:
        events = events.filter(title__icontains=query)
    return render(request, 'pages/home.html', {'events': events})


def event_details(request, event_id):
    """عرض تفاصيل حدث معين"""
    event = get_object_or_404(Event, id=event_id)
    return render(request, "pages/event_details.html", {"event": event})


@login_required
def reserve_ticket(request, event_id):
    """حجز تذكرة"""
    event = get_object_or_404(Event, id=event_id)
    if event.available_tickets > 0:
        ticket = Ticket.objects.create(user=request.user, event=event, is_reserved=True)
        event.available_tickets -= 1
        # event.tickets_sold += 1
        event.save()
        return redirect('view_reserved_tickets')
    else:
        return render(request, 'events/event_not_available.html')


@login_required
def view_reserved_tickets(request):
    """عرض التذاكر المحجوزة للمستخدم الحالي"""
    tickets = Ticket.objects.filter(user=request.user, is_reserved=True, is_refunded=False)
    return render(request, 'events/reserved_tickets.html', {'tickets': tickets})


@login_required
def refund_ticket(request, ticket_id):
    """استرداد تذكرة"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user, is_refunded=False)
    ticket.is_refunded = True
    ticket.event.available_tickets += 1
    ticket.event.tickets_sold -= 1
    ticket.event.save()
    ticket.save()
    return redirect('view_reserved_tickets')
