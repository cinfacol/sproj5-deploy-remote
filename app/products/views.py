from itertools import product
from django.shortcuts import render
from django.views import generic

from .models import Product, Media

namespace = "products"


class ProductListView(generic.ListView):

    model = Product

    def get(self, request):
        products = Product.objects.all()
        products_images = products.filter(imagenes__default=True)

        context = {
            "products": products,
            "images": products_images,
        }

        return render(request, "products/product_list.html", context)


class MediaDetailView(generic.DetailView):

    model = Product
    template_name = "products/product_detail.html"
