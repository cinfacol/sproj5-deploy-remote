from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_detail'),
    path('increase-quantity/<pk>/',
         views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/',
         views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/',
         views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', login_required(views.CheckoutView.as_view()), name='checkout'),
    path('payment/', login_required(views.PaymentView.as_view()), name='payment'),
    path('thanks/', views.ThankYouView.as_view(), name='thanks'),
]
