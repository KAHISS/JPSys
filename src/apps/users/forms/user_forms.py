from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

TAILWIND_INPUT_CLASS = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all placeholder-zinc-600'


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'type', 'document', 'phone', 'addres', 'city'
        )
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'document': forms.TextInput(attrs={'placeholder': 'Apenas números'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = TAILWIND_INPUT_CLASS


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'type', 'document', 'phone', 'addres', 'city'
        )
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'document': forms.TextInput(attrs={'placeholder': 'Apenas números'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = TAILWIND_INPUT_CLASS
