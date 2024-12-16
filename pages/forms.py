from django import forms

from .models import Cart, Event, Payment, RefundRequest, Ticket, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    # إذا أردت إضافة تحقق من الـ role يمكن إضافته هنا
    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ['regular', 'publisher', 'admin']:
            raise forms.ValidationError("Invalid role selected.")
        return role

# class PublisherProfileForm(forms.ModelForm):
#     class Meta:
#         model = PublisherProfile
#         fields = ['organization_name']

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
            'date': forms.DateInput(attrs={'type': 'date', 'lang': 'en'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'lang': 'en'}),
        }
        

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event']
        
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)  # Get the event passed during form initialization
        super(TicketForm, self).__init__(*args, **kwargs)
        if event:
            self.fields['event'].initial = event  # Set the initial value for the event field
            self.fields['event'].widget = forms.HiddenInput()  # Hide the field

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = ['ticket', 'status']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['items']
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(choices=Payment._meta.get_field('payment_method').choices)
        }
        
