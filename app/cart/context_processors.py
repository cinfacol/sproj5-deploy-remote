from .cart import get_or_set_order_session


def cart(request):
    return {'cart': get_or_set_order_session(request)}
