from django.urls import path

from .views import CategoryListView, DetalleView, HomeView

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<slug:slug>/', DetalleView.as_view(), name="detail"),
    path('<slug:category_slug>/',
         CategoryListView.as_view(), name="category_list"),
]
