import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse

from .models import Cart, Event, Payment, Ticket, User

# class TestUser(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user_data = {
#             "email": "testuser@example.com",
#             "password": "TestPassword123",
#             "role": "regular",
#         }
#         self.user = User.objects.create(
#             email=self.user_data["email"],
#             username="testuser",
#             password=make_password(self.user_data["password"]),
#             role=self.user_data["role"],
#         )

#     def test_user_creation(self):
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(self.user.email, self.user_data["email"])

#     def test_login(self):
#         response = self.client.post(
#             reverse("login_view"),
#             {"email": self.user_data["email"], "password": self.user_data["password"]},
#         )
#         self.assertEqual(response.status_code, 302)  # Successful login redirects

# class TestEvent(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.publisher = User.objects.create(
#             email="publisher@example.com",
#             username="publisher",
#             password=make_password("PublisherPassword123"),
#             role="publisher",
#         )
#         self.event = Event.objects.create(
#             title="Test Event",
#             description="This is a test event.",
#             date="2024-12-10",
#             time="14:00:00",
#             location="Test Location",
#             price=50.0,
#             available_tickets=100,
#         )

#     def test_event_creation(self):
#         self.assertEqual(Event.objects.count(), 1)
#         self.assertEqual(self.event.title, "Test Event")

#     def test_event_details_view(self):
#         response = self.client.get(reverse("event_details", args=[self.event.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.event.title)

# class TestTicket(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             email="buyer@example.com",
#             username="buyer",
#             password=make_password("BuyerPassword123"),
#             role="regular",
#         )
#         self.event = Event.objects.create(
#             title="Ticketed Event",
#             description="This is a ticketed event.",
#             date="2024-12-15",
#             time="18:00:00",
#             location="Event Location",
#             price=100.0,
#             available_tickets=50,
#         )

#     def test_ticket_purchase(self):
#         ticket = Ticket.objects.create(event=self.event, user=self.user, quantity=1)
#         ticket.purchase_ticket()
#         self.assertEqual(self.event.available_tickets, 49)

# class TestCart(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             email="cartuser@example.com",
#             username="cartuser",
#             password=make_password("CartUserPassword123"),
#             role="regular",
#         )
#         self.event = Event.objects.create(
#             title="Cart Event",
#             description="This is an event added to cart.",
#             date="2024-12-20",
#             time="20:00:00",
#             location="Cart Location",
#             price=150.0,
#             available_tickets=30,
#         )
#         self.cart = Cart.objects.create(user=self.user)

#     def test_add_to_cart(self):
#         self.cart.items.add(self.event)
#         self.assertEqual(self.cart.items.count(), 1)
#         self.assertIn(self.event, self.cart.items.all())

#     def test_cart_total_price(self):
#         self.cart.items.add(self.event)
#         self.assertEqual(self.cart.total_price(), 150.0)

# class TestPayment(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(
#             email="payuser@example.com",
#             username="payuser",
#             password=make_password("PayUserPassword123"),
#             role="regular",
#         )
#         self.event = Event.objects.create(
#             title="Paid Event",
#             description="Event for payment test.",
#             date="2024-12-25",
#             time="17:00:00",
#             location="Payment Location",
#             price=200.0,
#             available_tickets=10,
#         )
#         self.ticket = Ticket.objects.create(event=self.event, user=self.user, quantity=1)

#     def test_payment_creation(self):
#         payment = Payment.objects.create(
#             amount=self.event.price,
#             payment_method="Sadad",
#             payment_status="completed",
#         )
#         payment.tickets.add(self.ticket)
#         # Assume processing the payment also involves purchasing tickets
#         self.ticket.purchase_ticket()  # Simulate ticket purchase
#         self.assertEqual(self.event.available_tickets, 9)  # Now this should be 9

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event, Ticket

User = get_user_model()

class EventViewsTestCase(TestCase):
    
    def setUp(self):
        # Set up the user and event for our tests
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='regular'  # Make sure to set the appropriate role
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event.',
            price=100.00,
            date='2024-12-31',
            time='20:00:00',
            location='Test Location',
            image='images/test_event.png'
        )
        # Log in the user
        self.client.login(username='testuser', password='password123')

    def test_search_event(self):
        response = self.client.get(reverse('search_event'), {'q': 'Test Event'})
        print("Test Search Event: Expected 'Test Event' in response.")
        if 'Test Event' in response.content.decode():
            print("Actual Output: 'Test Event' found in response.")
        else:
            print("Actual Output: 'Test Event' NOT found in response.")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')  # Check that the event is in the page

    def test_booked_events(self):
        # Book a ticket for the event
        Ticket.objects.create(user=self.user, event=self.event)
        response = self.client.get(reverse('booked_events'))
        print("Test Booked Events: Expected 'Test Event' in booked events.")
        if 'Test Event' in response.content.decode():
            print("Actual Output: 'Test Event' found in booked events.")
        else:
            print("Actual Output: 'Test Event' NOT found in booked events.")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')  # Check that the booked event is present

    def test_delete_booking(self):
        # Book a ticket and then delete it
        ticket = Ticket.objects.create(user=self.user, event=self.event)
        response = self.client.post(reverse('delete_booking', args=[ticket.id]))
        print("Test Delete Booking: Expected ticket to be deleted.")
        # Check that the ticket no longer exists
        response = self.client.get(reverse('booked_events'))
        if ticket.event.title not in response.content.decode():
            print(f"Actual Output: Ticket '{ticket.event.title}' has been deleted successfully.")
        else:
            print(f"Actual Output: Ticket '{ticket.event.title}' is still present.")
        self.assertNotContains(response, ticket.event.title)  # Verify that the event title is not in the response
