from cart.cart import get_or_set_order_session
from cart.forms import AddToCartForm
from django.shortcuts import get_object_or_404, render, reverse
from django.views import generic
from django.views.generic import ListView
from products.models import Category

from .models import Articulo

namespace = 'store'


class HomeView(ListView):
    queryset = Articulo.newmanager.all()
    context_object_name = 'articulos'
    paginate_by = 4
    template_name = 'index.html'


class DetalleView(generic.FormView):
    template_name = 'detail.html'
    model = Articulo
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Articulo, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse('cart:cart_detail')

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        item_filter = order.items.filter(product=product)
        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()

        return super(DetalleView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DetalleView, self).get_context_data(**kwargs)

        context["post"] = self.get_object()
        context["images"] = context["post"].product.imagenes.all()[:3]

        return context


class CategoryListView(ListView):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        articulos = Articulo.newmanager.all()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            articulos = Articulo.objects.filter(category=category)

        context = {
            'category': category,
            'categories': categories,
            'articulos': articulos
        }

        return render(request, 'categories.html', context)
