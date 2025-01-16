from .models import Cart,Order

def cart_item_count(request):
    total_items = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        for item in cart.items.all():
            total_items += item.quantity
    return {'cart_item_count': total_items}

def order_item_count(request):
    if request.user.is_authenticated:
        total_orders = Order.objects.filter(user=request.user, status__in=['pending', 'waiting for payment','shipped','paid']).count()
    else:
        total_orders = 0
    return {'order_item_count': total_orders}
