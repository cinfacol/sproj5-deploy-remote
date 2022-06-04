import datetime

from django import forms
from django.forms.widgets import NumberInput

from .models import Address, Profile, UserBase


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ["shipping_address",
                  "billing_address", "ciudad", "departamento", "zip"]

    def __init__(self, *args, **kwargs):
        # user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        self.fields["shipping_address"].widget.attrs.update(
            {"class": "form-control mb-2 account-form",
                "placeholder": "Tu dirección de envío"}
        )
        self.fields["billing_address"].required = False
        self.fields["billing_address"].widget.attrs.update(
            {"class": "form-control mb-2 account-form",
                "placeholder": "Dirección de tu oficina (opcional)"}
        )
        self.fields["ciudad"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Tu ciudad"}
        )
        self.fields["departamento"].widget.attrs.update(
            {"class": "form-control mb-2 account-form",
                "placeholder": "Tu departamento"}
        )
        self.fields["zip"].widget.attrs.update(
            {"class": "form-control mb-2 account-form",
                "placeholder": "Código Postal"}
        )


class UserEditAccountForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email and username (can not be changed)', max_length=200, widget=forms.EmailInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='First name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Last Name', min_length=4, max_length=50, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'username', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True


GENDER_CHOICE = (
    ('male', 'Hombre'),
    ('female', 'Mujer'),
)


class UserEditProfileForm(forms.ModelForm):

    picture = forms.ImageField(
        label='Profile Picture', required=False, widget=forms.FileInput(
            attrs={'class': 'form-control mb-3', 'id': 'picture-url'}))
    banner = forms.ImageField(
        label='Profile Banner', required=False, widget=forms.FileInput(
            attrs={'class': 'form-control mb-3', 'id': 'banner-url'}))
    url = forms.URLField(
        label='Website Url', max_length=50, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Url', 'id': 'form-url'}))
    birthday = forms.DateField(
        label='Birthday', required=False, initial=datetime.date.today, widget=NumberInput(
            attrs={'class': 'form-control mb-3', 'type': 'date', 'id': 'form-birthday'}))
    gender = forms.ChoiceField(
        label='Gender', required=False, choices=GENDER_CHOICE, widget=forms.Select(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Género', 'id': 'form-gender'}))
    bio = forms.CharField(
        label='Bio', min_length=4, max_length=250, required=False, widget=forms.Textarea(
            attrs={'class': 'form-control mb-3', 'rows': 3, 'placeholder': 'Biografía', 'id': 'form-bio'}))
    phone = forms.CharField(
        label='Phone *', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Phone', 'id': 'form-phone'}))
    mobile = forms.CharField(
        label='Mobile', min_length=4, max_length=50, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'mobile', 'id': 'form-mobile'}))

    class Meta:
        model = Profile
        fields = ('picture', 'banner', 'url',
                  'birthday', 'gender', 'bio', 'phone', 'mobile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = True
