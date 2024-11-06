from django import forms

from .models import (Event, Payment, PublisherProfile, RefundRequest,
                     SiteAdminProfile, Ticket, User)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

class PublisherProfileForm(forms.ModelForm):
    class Meta:
        model = PublisherProfile
        fields = ['organization_name']

# class SiteAdminProfileForm(forms.ModelForm):
#     class Meta:
#         model = SiteAdminProfile
#         #later add admin_permissions field

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image']

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description',"image", 'date', 'time', 'location', 'price', 'available_tickets']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'user']

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = ['ticket', 'credit_amount', 'status']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['ticket', 'amount', 'payment_method']
