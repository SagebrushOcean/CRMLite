from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("attach-user-to-company/", views.AttachUserView.as_view(), name="attach-user"),
    path("unattach-user-from-company/", views.UnattachUserView.as_view(), name="unattach-user"),
    path("company-staff-list/", views.StaffListView.as_view(), name="staff-list"),
]