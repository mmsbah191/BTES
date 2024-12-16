# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_details, name='event_details'),
    path('events/<int:event_id>/reserve/', views.reserve_ticket, name='reserve_ticket'),
    path('reserved-tickets/', views.view_reserved_tickets, name='view_reserved_tickets'),
    path('refund-ticket/<int:ticket_id>/', views.refund_ticket, name='refund_ticket'),
]
