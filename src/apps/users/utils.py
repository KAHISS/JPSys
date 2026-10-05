# apps/users/utils.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Inclui is_active no hash: assim que o usuário verifica,
        # o token vira inválido automaticamente (não reutilizável)
        return f"{user.pk}{timestamp}{user.is_active}{user.password}"


email_verification_token = EmailVerificationTokenGenerator()


def send_verification_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    verify_path = reverse('users:verify_email', kwargs={
                          'uidb64': uidb64, 'token': token})
    verify_url = f"{settings.SITE_URL}{verify_path}"

    context = {'user': user, 'verify_url': verify_url}
    subject = 'Confirme seu email - JP Acessórios'
    text_body = render_to_string('users/emails/verify_email.txt', context)
    html_body = render_to_string('users/emails/verify_email.html', context)

    email = EmailMultiAlternatives(
        subject, text_body, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)
