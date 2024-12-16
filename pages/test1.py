import os

apps = ["users", "events", "tickets", "cart", "payments", "refunds"]

for app in apps:
    os.system(f"python manage.py startapp {app}")
