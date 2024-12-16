from pages.models import User


class UserFactory:
    @staticmethod
    def create_user(user_type, email, password):
        if user_type == "regular":
            user = User(email=email, password=password, role="regular")
        elif user_type == "publisher":
            user = User(email=email, password=password, role="publisher")
        elif user_type == "admin":
            user = User(email=email, password=password, role="admin")
        else:
            raise ValueError("Invalid user type")
        return user

class PaymentFactory:
    @staticmethod
    def create_payment(payment_method, tickets, amount):
        if payment_method == "Sadad":
            return SadadPayment(tickets, amount)
        elif payment_method == "Edfa3li":
            return Edfa3liPayment(tickets, amount)
        else:
            raise ValueError("Unsupported payment method")

class Payment:
    def __init__(self, tickets, amount):
        self.tickets = tickets
        self.amount = amount

    def process_payment(self):
        raise NotImplementedError("This method should be overridden in subclasses.")

class SadadPayment(Payment):
    def process_payment(self):
        return f"Processing Sadad payment for {self.amount}."

class Edfa3liPayment(Payment):
    def process_payment(self):
        return f"Processing Edfa3li payment for {self.amount}."
