from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('snack', 'Snack'),
        ('drink', 'Drink'),
    ]
    SUBCATEGORY_CHOICES = [
        # Snacks
        ('chips', 'Chips'),
        ('cookies', 'Cookies'),
        ('jerky', 'Jerky'),
        ('bars', 'Bars'),
        ('nuts', 'Nuts & Trail Mix'),
        ('gluten', 'Gluten Free'),
        # Drinks
        ('soda', 'Soda'),
        ('energy_drink', 'Energy Drink'),
        ('juice', 'Juice'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, null=False, blank=False, default='snack')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    sub_category = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, null=False, blank=False,
                                    default='chips')
    ingredients = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)

    # Snack
    weight = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    # Drink
    volume = models.PositiveIntegerField(blank=True, null=True)
    is_alcoholic = models.BooleanField(blank=True, null=True, default=False)

    def clean(self):

        if self.category == 'drink':
            if self.sub_category in ['chips', 'cookies', 'jerky', 'bars', 'nuts', 'gluten']:
                raise ValidationError("Sub-category must be a valid drink option for a drink product.")
            if not self.volume:
                raise ValidationError('Volume is required for drinks.')
            if self.weight:
                raise ValidationError('Weight should not be specified for a drink.')


        elif self.category == 'snack':
            if self.sub_category in ['soda', 'energy_drink', 'juice']:
                raise ValidationError("Sub-category must be a valid snack option for a snack product.")
            if not self.weight:
                raise ValidationError('Weight is required for snacks.')
            if self.volume:
                raise ValidationError('Volume should not be specified for a snack.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('', max_length=2000)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'{self.product.name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.item_sum
        self.total_price = total
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('waiting for payment', 'Waiting for Payment'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} order'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart_items')
    item_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_item_sum(self):
        self.item_sum = self.quantity * self.price
        self.save()

    def __str__(self):
        return ""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return ""

