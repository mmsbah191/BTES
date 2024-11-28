from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Event, Ticket, Cart, Payment, RefundRequest
from django.contrib.auth.hashers import make_password

class TestUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            "email": "testuser@example.com",
            "password": "TestPassword123",
            "role": "regular",
        }
        self.user = User.objects.create(
            email=self.user_data["email"],
            username="testuser",
            password=make_password(self.user_data["password"]),
            role=self.user_data["role"],
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, self.user_data["email"])

    def test_login(self):
        response = self.client.post(
            reverse("login_view"),
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        self.assertEqual(response.status_code, 302)  # Successful login redirects

class TestEvent(TestCase):
    def setUp(self):
        self.client = Client()
        self.publisher = User.objects.create(
            email="publisher@example.com",
            username="publisher",
            password=make_password("PublisherPassword123"),
            role="publisher",
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            date="2024-12-10",
            time="14:00:00",
            location="Test Location",
            price=50.0,
            available_tickets=100,
        )

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.title, "Test Event")

    def test_event_details_view(self):
        response = self.client.get(reverse("event_details", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

class TestTicket(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email="buyer@example.com",
            username="buyer",
            password=make_password("BuyerPassword123"),
            role="regular",
        )
        self.event = Event.objects.create(
            title="Ticketed Event",
            description="This is a ticketed event.",
            date="2024-12-15",
            time="18:00:00",
            location="Event Location",
            price=100.0,
            available_tickets=50,
        )

    def test_ticket_purchase(self):
        ticket = Ticket.objects.create(event=self.event, user=self.user, quantity=1)
        ticket.purchase_ticket()
        self.assertEqual(self.event.available_tickets, 49)

class TestCart(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email="cartuser@example.com",
            username="cartuser",
            password=make_password("CartUserPassword123"),
            role="regular",
        )
        self.event = Event.objects.create(
            title="Cart Event",
            description="This is an event added to cart.",
            date="2024-12-20",
            time="20:00:00",
            location="Cart Location",
            price=150.0,
            available_tickets=30,
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_add_to_cart(self):
        self.cart.items.add(self.event)
        self.assertEqual(self.cart.items.count(), 1)
        self.assertIn(self.event, self.cart.items.all())

    def test_cart_total_price(self):
        self.cart.items.add(self.event)
        self.assertEqual(self.cart.total_price(), 150.0)

class TestPayment(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email="payuser@example.com",
            username="payuser",
            password=make_password("PayUserPassword123"),
            role="regular",
        )
        self.event = Event.objects.create(
            title="Paid Event",
            description="Event for payment test.",
            date="2024-12-25",
            time="17:00:00",
            location="Payment Location",
            price=200.0,
            available_tickets=10,
        )
        self.ticket = Ticket.objects.create(event=self.event, user=self.user, quantity=1)

    def test_payment_creation(self):
        payment = Payment.objects.create(
            amount=self.event.price,
            payment_method="Sadad",
            payment_status="completed",
        )
        payment.tickets.add(self.ticket)
        # Assume processing the payment also involves purchasing tickets
        self.ticket.purchase_ticket()  # Simulate ticket purchase
        self.assertEqual(self.event.available_tickets, 9)  # Now this should be 9
