from django.contrib.auth.forms import SetPasswordForm

class AdminSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # O mesmo padrão de estilo Tailwind que você já usa nos outros forms
        default_class = 'w-full bg-black/50 border border-zinc-800 text-zinc-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all placeholder-zinc-600'
        
        for field in self.fields.values():
            field.widget.attrs['class'] = default_class