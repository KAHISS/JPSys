from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from utils.django_forms import add_placeholder

User = get_user_model()

TAILWIND_INPUT_CLASS = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all placeholder-zinc-600'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    terms = forms.BooleanField(
        required=True,
        label='Aceito os Termos de Uso e a Política de Privacidade'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'terms':
                field.widget.attrs['class'] = 'h-4 w-4 rounded border-zinc-700 bg-zinc-950 text-amber-500 focus:ring-amber-500'
            else:
                field.widget.attrs['class'] = TAILWIND_INPUT_CLASS
        add_placeholder(self.fields['email'], 'seuemail@exemplo.com')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe uma conta com esse email.')
        if "+" in email:
            raise forms.ValidationError('Não é permitido o uso de alias')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = User.Type.CLIENT
        user.is_active = False  # bloqueado até confirmar o email
        if commit:
            user.save()
        return user
