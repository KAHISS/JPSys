from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from apps.users.forms import LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    form = LoginForm()
    return render(request, 'users/pages/login.html', {
        'form': form,
        'form_action': reverse('users:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404("No POST data found.")

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )

        if authenticate_user is not None:
            messages.success(request, 'Login realizado com sucesso!')
            login(request, authenticate_user)
            if request.user.is_superuser:
                return redirect(reverse('inventory:inventory_list'))
            elif request.user.type == "promoter":
                return redirect(reverse('sales:promoters_sales_list'))
            elif request.user.type == "client":
                return redirect(reverse('sales:orders_sales_list'))

        else:
            messages.error(request, 'Credenciais inválidas!')
            return redirect(reverse('users:login'))
    else:
        messages.error(request, 'Erro ao validar formulário!')
        return redirect(reverse('users:login'))


@login_required(login_url='users:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        raise Http404("No POST data found.")

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('users:login'))

    logout(request)
    return redirect(reverse('users:login'))
