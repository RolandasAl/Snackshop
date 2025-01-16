from django.urls import path
from . import views
from .views import update_quantity, remove_item

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<str:sub_category>/', views.product_list, name='product_list_by_sub_category'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('my_cart/', views.my_cart, name='my_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('user-profile/', views.profile, name='user_profile'),
    path('update_quantity/<int:item_id>/<str:action>/', update_quantity, name='update_quantity'),
    path('remove_item/<int:item_id>/', remove_item, name='remove_item'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('orders/pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('orders/<int:order_id>/shipping-details/', views.shipping_details, name='shipping_details'),

]