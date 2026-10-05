from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from apps.users.forms import LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from apps.users.forms import RegisterForm
from apps.users.utils import email_verification_token, send_verification_email
from django.contrib.auth import get_user_model


User = get_user_model()


def register_view(request):
    form = RegisterForm()
    return render(request, 'users/pages/register.html', {
        'form': form,
        'form_action': reverse('users:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404("No POST data found.")

    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.type = User.Type.CLIENT
        user.save()
        send_verification_email(request, user)
        messages.success(
            request,
            'Cadastro realizado! Verifique seu email para ativar sua conta.'
        )
        return redirect(reverse('users:login'))
    else:
        for error in form.errors.values():
            messages.error(request, error.as_text())
        return render(request, 'users/pages/register.html', {
            'form': form,
            'form_action': reverse('users:register_create')
        })


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        messages.success(request, 'Email confirmado com sucesso! Faça login.')
    else:
        messages.error(request, 'Link de confirmação inválido ou expirado.')

    return redirect(reverse('users:login'))


def resend_verification_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email__iexact=email, is_active=False)
            send_verification_email(request, user)
            messages.success(request, 'Novo email de confirmação enviado.')
        except User.DoesNotExist:
            messages.success(
                request, 'Se o email existir e estiver pendente, enviamos o link novamente.')
        return redirect(reverse('users:login'))

    return render(request, 'users/pages/resend_verification.html')


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
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        authenticate_user = authenticate(
            username=username,
            password=password
        )

        if authenticate_user is not None:
            messages.success(request, 'Login realizado com sucesso!')
            login(request, authenticate_user)

            next_url = request.POST.get('next') or request.GET.get('next')

            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            if request.user.is_superuser:
                return redirect(reverse('inventory:inventory_list'))
            elif request.user.type == "promoter":
                return redirect(reverse('sales:promoters_sales_list'))
            else:  # Considerando cliente como padrão se falhar os de cima
                return redirect(reverse('sales:orders_sales_list'))

        else:
            # Verifica se a conta existe mas está inativa (email não confirmado)
            user_exists = User.objects.filter(
                username=username, is_active=False).exists()
            if user_exists:
                messages.error(
                    request, 'Confirme seu email antes de fazer login.')
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
