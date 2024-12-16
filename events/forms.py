from django import forms

from pages.models import Event, Ticket


class TicketReservationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event']
