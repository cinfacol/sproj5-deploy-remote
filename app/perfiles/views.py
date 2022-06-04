from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View

from .forms import UserAddressForm, UserEditAccountForm, UserEditProfileForm
from .models import Address, Profile, UserBase

app_name = "perfiles"


class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(UserBase, username=username)
        profile = Profile.objects.get(user=user)
        addresses = Address.objects.filter(user=user, default=True)

        context = {
            'user': user,
            'profile': profile,
            "addresses": addresses,
        }
        return render(request, 'perfiles/detail.html', context)


@login_required
def edit_profile(request):

    usuario = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        user_form = UserEditAccountForm(
            instance=request.user, data=request.POST)
        profile_form = UserEditProfileForm(
            data=request.POST, files=request.FILES, instance=usuario)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            messages.success(
                request,  'Your profile has been successfully updated')
        else:
            messages.error(
                request,  'Your profile can not be updated')
    else:
        user_form = UserEditAccountForm(instance=request.user)
        profile_form = UserEditProfileForm(instance=usuario)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': usuario
    }

    return render(request, 'perfiles/edit_profile.html', context)

# Addresses


@login_required
def view_address(request):
    addresses = Address.objects.filter(user=request.user)
    context = {
        "addresses": addresses,
        "usuario": request.user
    }
    return render(request, "perfiles/addresses.html", context)


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("perfiles:direcciones"))
    else:
        address_form = UserAddressForm()

    profile = Profile.objects.get(user=request.user)
    context = {
        "form": address_form,
        'profile': profile,
    }

    return render(request, "perfiles/edit_addresses.html", context)


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("perfiles:direcciones"))
    else:
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "perfiles/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, user=request.user).delete()
    return redirect("perfiles:direcciones")


@login_required
def set_default(request, id):
    Address.objects.filter(user=request.user,
                           default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    return redirect("perfiles:direcciones")
