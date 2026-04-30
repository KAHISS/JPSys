from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(
            attrs={'class': 'w-full bg-[#1A1D20] border border-gray-700 text-gray-200 text-base rounded-lg focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent block pl-5 p-3 transition-colors outline-none'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={'class': 'w-full bg-[#1A1D20] border border-gray-700 text-gray-200 text-base rounded-lg focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent block pl-5 p-3 transition-colors outline-none'})
    )

    class Meta:
        fields = ['username', 'password']
