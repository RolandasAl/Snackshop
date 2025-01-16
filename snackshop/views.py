from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from .forms import ProductReviewForm, ShippingForm
from .models import Product, ProductReview, Cart, CartItem, Order, OrderItem


def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'user_profile.html')

def product_list(request, sub_category):
    products = Product.objects.filter(category__in=['snack', 'drink'], sub_category=sub_category).order_by('name')

    brand_filter = request.GET.get('brand')
    if brand_filter:
        products = products.filter(brand=brand_filter)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    brands = Product.objects.filter(sub_category=sub_category).values_list('brand', flat=True).distinct()

    context = {
        'products': page_obj,
        'sub_category': sub_category,
        'brands': brands,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = ProductReview.objects.filter(product=product)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.reviewer = request.user
            review.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductReviewForm()

    return render(request, 'product_detail.html', {'product': product,'reviews': reviews,'form': form,})


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'A user with the email {email} is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f'User {username} has been successfully registered!')

        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

    return render(request, 'register.html')

@login_required
def my_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'my_cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    referer = request.META.get('HTTP_REFERER', '/')
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock!")
        return redirect(referer)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1, 'price': product.price})
    if item_created:
        item.calculate_item_sum()
    else:
        if item.quantity < product.stock:
            item.quantity += 1
            item.calculate_item_sum()
        else:
            messages.error(request, f"Sorry, only {product.stock} of {product.name} is available.")
        item.save()
    messages.success(request, f'{product.name} has been added to your cart.')

    cart.calculate_total_price()

    return redirect(referer)


@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == 'increase':
        if item.quantity < item.product.stock:
            item.quantity += 1
            item.calculate_item_sum()
            messages.success(request, f"Quantity of {item.product.name} increased to {item.quantity}.")
        else:
            messages.error(request, f"Sorry, only {item.product.stock} of {item.product.name} is available.")
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.calculate_item_sum()
            messages.success(request, f"Quantity of {item.product.name} decreased to {item.quantity}.")
        else:
            messages.error(request, f"Cannot reduce quantity below 1. Remove the item instead.")
    item.save()
    cart = item.cart
    cart.calculate_total_price()

    return redirect('my_cart')


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    cart = item.cart
    cart.calculate_total_price()
    messages.success(request, f"{product_name} has been removed from your cart.")
    return redirect('my_cart')


@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)

    order = Order.objects.create(user=request.user, status='waiting for payment')

    for cart_item in cart.items.all():
        order_item = OrderItem(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.price,
            item_sum=cart_item.item_sum,
        )

        order_item.save()
        cart_item.product.stock -= cart_item.quantity
        cart_item.product.save()

    order.final_price = cart.total_price
    order.save()
    cart.items.all().delete()
    cart.calculate_total_price()

    messages.success(request, "Your order has been placed successfully.")
    return redirect('my_orders')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, status__in=['pending', 'waiting for payment', 'paid', 'shipped'])
    completed_orders = Order.objects.filter(user=request.user, status__in=['completed'])

    context = {
        'orders': orders,
        'completed_orders': completed_orders,
    }

    return render(request, 'my_orders.html', context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status != 'Completed':
        for item in order.order_items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        order.delete()
        messages.success(request, "Order has been canceled and stock updated.")
    else:
        messages.error(request, "Completed orders cannot be canceled.")
    return redirect('my_orders')


def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'waiting for payment':
        order.status = 'paid'
        order.save()
        messages.success(request, "Order status has been updated to Paid.")
    else:
        messages.error(request, "Only orders with status 'Waiting for Payment' can be paid.")
    return redirect('my_orders')


@login_required
def shipping_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('my_orders')

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('my_orders')
    else:
        form = ShippingForm(instance=order)
    return render(request, 'shipping_details.html', {'form': form, 'order': order})
