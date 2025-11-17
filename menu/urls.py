from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("services/<int:service_id>/", views.service_detail, name="service_detail"),
    path("contact/", views.contact, name="contact"),
    path("test-404/", views.test_404, name="test_404"),
]
