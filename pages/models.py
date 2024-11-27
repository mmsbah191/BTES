import os
from datetime import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ("regular", "Regular User"),
            ("publisher", "Publisher"),
            ("admin", "Admin"),
        ],
        default="regular",
    )  # A field to specify the user role

    # Function to return path for the profile image upload
    def get_profile_image_path(instance, filename):
        extension = os.path.splitext(filename)[1]
        return f"profile{extension}"

    profile_image = models.ImageField(
        upload_to=get_profile_image_path, default="profile.png", blank=True
    )

    def is_publisher(self):
        return self.role == "publisher"

    def is_admin(self):
        return self.role == "admin"


class PublisherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255, blank=True, null=True)


class SiteAdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_permissions = models.TextField()  # Define special permissions if needed


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)
    date = models.DateField(default="2024-12-06")
    time = models.TimeField(default="20:45:00")
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    available_tickets = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.title} {self.description[:30]}..."


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_refunded = models.BooleanField(default=False)

    def purchase_ticket(self):
        # Check if enough tickets are available
        if self.event.available_tickets >= self.quantity:
            self.event.available_tickets -= self.quantity  # Subtract the purchased tickets from the event
            self.is_refunded = False
            self.save()  # Save the ticket
            self.event.save()  # Save the event after updating ticket count
        else:
            raise ValueError("Not enough tickets available for this event.")

    def __str__(self):
        return f"Ticket for {self.event.title} - Purchased by {self.user.username}"


class Payment(models.Model):
    tickets = models.ManyToManyField(Ticket)  # Payment may involve multiple tickets
    payment_date = models.DateTimeField(auto_now_add=True)  # Payment date
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Paid amount
    payment_method = models.CharField(
        max_length=50,
        choices=[("Sadad", "Sadad"), ("Edfa3li", "Edfa3li")],
    )  # Payment methods
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
        default="pending",
    )  # Payment status
    transaction_id = models.CharField(
        max_length=255, blank=True, null=True
    )  # External transaction ID
    total_tickets = models.IntegerField(
        default=0
    )  # Total number of deducted tickets (indicating the number of tickets)

    # Logic for processing payment and deducting tickets
    def process_payment(self):
        if self.payment_status != "completed":
            raise ValueError("Payment is not completed yet.")

        total_deducted = 0
        for ticket in self.tickets.all():
            if ticket.event.available_tickets >= ticket.quantity:
                ticket.event.available_tickets -= ticket.quantity  # Deduct tickets from event
                ticket.save()
                total_deducted += ticket.quantity
            else:
                raise ValueError(
                    f"Not enough tickets available for the event: {ticket.event.title}"
                )

        self.total_tickets = total_deducted  # Record the number of deducted tickets
        self.save()  # Save the payment after processing

    def __str__(self):
        return f"Payment for {self.total_tickets} tickets on {self.payment_date} via {self.payment_method}"


# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # ربط الحجز بالمستخدم
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)  # ربط الحجز بالحدث
#     created_at = models.DateTimeField(default=timezone.now)  # وقت إنشاء الحجز

#     def __str__(self):
#         return f"Booking for {self.event.title} by {self.user.username}"
    
class RefundRequest(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("cancelled", "Cancelled"), ("completed", "Completed")],
    )
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Refund request for {self.ticket}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Event)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"
