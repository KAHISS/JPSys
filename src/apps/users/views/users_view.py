from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apps.users.forms import CustomUserCreationForm, CustomUserChangeForm
from utils.pagination import make_pagination
from apps.users.filters import UserFilter

User = get_user_model()

PER_PAGE = 10


@login_required(login_url='users:login', redirect_field_name='next')
def users_list(request):
    # 1. Verifica permissão
    if not request.user.is_superuser:
        messages.error(
            request, f"Você está logado como {request.user.username}, mas precisa ser um administrador para acessar esta página.")
        return redirect('users:login')

    queryset = User.objects.all().order_by('-id')

    user_filter = UserFilter(request.GET, queryset=queryset)

    users, pagination_range = make_pagination(
        request, user_filter.qs, PER_PAGE)

    get_copy = request.GET.copy()

    if 'page' in get_copy:
        del get_copy['page']

    additional_url_query = '&' + get_copy.urlencode() if get_copy else ''

    return render(request, 'users/pages/users.html', context={
        'page_title': 'Busca Avançada',
        'pagination_range': pagination_range,
        'objects': users,
        'additional_url_query': additional_url_query,
        'user_active': 'bg-amber-500 text-black font-semibold',
        'filter': user_filter,
        'title': 'Usuários Cadastrados',
        "page": "users"
    })


@login_required(login_url='users:login', redirect_field_name='next')
def user_form_view(request, pk=None):
    if not request.user.is_superuser:
        raise Http404("Você não tem permissão para acessar esta página.")

    if request.method == 'POST' and 'delete' in request.POST and pk:
        user_to_delete = get_object_or_404(User, id=pk)

        if user_to_delete == request.user:
            messages.error(
                request, "Você não pode excluir a sua própria conta.")
            return redirect('users:users_list')

        nome_usuario = user_to_delete.username
        user_to_delete.delete()
        messages.success(
            request, f"Usuário '{nome_usuario}' excluído com sucesso!")
        return redirect('users:users_list')

    if pk:
        # Modo de Edição
        user_instance = get_object_or_404(User, id=pk)
        title = f"Editar Usuário - {user_instance.username}"
        path = f"Usuários > Editar > {user_instance.username}"
        action = "update"
        indentifier = user_instance.id
        print(indentifier)

        form = CustomUserChangeForm(
            request.POST or None, instance=user_instance)
    else:
        # Modo de Criação
        user_instance = None
        title = "Registrar Novo Usuário"
        path = "Usuários > Registrar Usuário"
        action = "create"
        indentifier = None

        form = CustomUserCreationForm(request.POST or None)

    if request.method == 'POST' and not 'delete' in request.POST:
        if form.is_valid():
            user = form.save(commit=False)

            if user.type == User.Type.ADMIN:
                user.is_staff = True
                user.is_superuser = True
            elif user.type == User.Type.PROMOTER:
                user.is_staff = True
                user.is_superuser = False
            elif user.type == User.Type.CLIENT:
                user.is_staff = False
                user.is_superuser = False

            user.save()

            messages.success(
                request, f"Usuário {'atualizado' if pk else 'registrado'} com sucesso!")
            return redirect('users:users_list')
        else:
            messages.error(
                request, "Erro ao processar o formulário. Verifique os dados fornecidos.")

    return render(request, 'users/pages/user_form.html', context={
        "section": "users",  # Para controle do menu lateral ativo
        "form": form,
        "title": title,
        "path": path,
        "action": action,
        "indentifier": indentifier,
        "back_url": reverse('users:users_list'),
        'user_active': 'bg-amber-500 text-black font-semibold',
        "page": "users-form"
    })
