import datetime
import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from perfiles.forms import UserAddressForm
from perfiles.models import Address
from store.models import Articulo

from .cart import get_or_set_order_session
from .models import OrderItem, Payment


class CartView(generic.TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        cart = context["order"]
        context["post"] = cart.items.all()
        return context


def cart_remove(request, product_id):
    cart = get_or_set_order_session(request)
    product = get_object_or_404(Articulo, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class CheckoutView(generic.FormView):
    template_name = 'cart/checkout.html'
    form_class = UserAddressForm

    """ def get_success_url(self):
        return reverse("cart:pyment") """

    """ def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs """

    def get_context_data(self, *args, **kwargs):
        addresses = Address.objects.filter(user=self.request.user)
        addr_default = False
        for addr in addresses:
            if addr.default:
                addr_default = True

        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        context['addresses'] = addresses
        context['addr_default'] = addr_default
        return context


class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("cart:cart_detail")


class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart:cart_detail")


class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:cart_detail")


class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        # context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context['order'] = get_or_set_order_session(self.request)
        context['CALLBACK_URL'] = self.request.build_absolute_uri(
            reverse("cart:thanks"))
        return context


class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body)
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            amount=float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='PayPal'
        )
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "Success"})


class ThankYouView(generic.TemplateView):
    template_engine = 'cart/thanks.html'
