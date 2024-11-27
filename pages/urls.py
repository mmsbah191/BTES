from django.urls import path

from pages import admin

from . import views
from .views import search_event

urlpatterns = [
    path("index/", views.index, name="index"),
    path("home/", views.home, name="home"),
    path(
        "update_profile_image/", views.update_profile_image, name="update_profile_image"
    ),
    path("create_event/", views.create_event, name="create_event"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path(
        "payment_confirmation/<int:event_id>/",
        views.payment_confirmation,
        name="payment_confirmation",
    ),
    path("", views.link_list, name="link_list"),
    path("checkout_event/<int:event_id>/", views.checkout_event, name="checkout_event"),
    path("checkout_card/", views.checkout_card, name="checkout_card"),
    path("event_details/<int:event_id>/", views.event_details, name="event_details"),
    path(
        "create_refund_request/",
        views.create_refund_request,
        name="create_refund_request",
    ),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout"),
    path("add_to_cart/<int:event_id>/", views.add_to_cart, name="add_to_cart"),
    path("view_cart/", views.view_cart, name="view_cart"),
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"),
    path(
        "delete_from_cart/<int:event_id>/",
        views.delete_from_cart,
        name="delete_from_cart",
    ),
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"),
    path("search-event/", views.search_event, name="search_event"),
    path("booked-events/", views.booked_events, name="booked_events"),
    path(
        "delete-booking/<int:booking_id>/", views.delete_booking, name="delete_booking"
    ),
]
