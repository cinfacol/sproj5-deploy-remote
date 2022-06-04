from django import forms

from .models import OrderItem

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class AddToCartForm(forms.ModelForm):
    # attributes = forms.ChoiceField()
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        model = OrderItem
        fields = ['quantity', 'override']
