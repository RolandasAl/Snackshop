from django.contrib import admin
from .models import Product, ProductReview, Cart, CartItem, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','brand','price')
    list_filter = ('category','sub_category','brand')
    search_fields = ('name','category')
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': (
            'name', 'description', 'price', 'category', 'image', 'stock', 'sub_category', 'ingredients', 'brand')
        }),
        ('Snack Information', {
            'fields': ('weight',),
        }),
        ('Drink Information', {
            'fields': ('volume', 'is_alcoholic'),
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    exclude = ('order',)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','total_price']
    inlines = [CartItemInline]
    fields = ('user','total_price')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'final_price')
    list_filter = ('status',)
    search_fields = ('user__username','id')
    inlines = [OrderItemInline]

    fields = ('user', 'status', 'created_at', 'city', 'address', 'postal_code', 'phone_number')
    readonly_fields = ('created_at',)

# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)







