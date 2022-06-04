from django.contrib.auth import views
from django.urls import path

from . import views
from .views import UserProfileView

app_name = "perfiles"

urlpatterns = [
    path("addresses/", views.view_address, name="direcciones"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/",
         views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/",
         views.set_default, name="set_default"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('<username>/', UserProfileView.as_view(), name="perfil")
]
