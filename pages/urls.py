from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("update_profile_image/", views.update_profile_image, name="update_profile_image"),
    path("", views.link_list, name="link_list"),  # رابط لعرض الروابط
    path("create_event/", views.create_event, name="create_event"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path(
        "create_refund_request/",
        views.create_refund_request,
        name="create_refund_request",
    ),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout"),
    path("create_payment/", views.create_payment, name="create_payment"),
]
