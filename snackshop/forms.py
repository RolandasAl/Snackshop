from django import forms
from .models import ProductReview, Order

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'content']

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'city', 'postal_code', 'phone_number']