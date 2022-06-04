from django.urls import path

from .views import ProductListView, MediaDetailView

app_name = "products"

urlpatterns = [
    path("<int:pk>", MediaDetailView.as_view(), name="media_detail"),
    path("", ProductListView.as_view(), name="products"),
]
