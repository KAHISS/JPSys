from django.db import models
from django.conf import settings


class LegalDocument(models.Model):
    class DocumentType(models.TextChoices):
        TERMS_OF_USE = 'terms_of_use', 'Terms of Use'
        PRIVACY_POLICY = 'privacy_policy', 'Privacy Policy'
        OTHER = 'other', 'Other'

    title = models.CharField(max_length=255, verbose_name='Title')
    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
        default=DocumentType.TERMS_OF_USE,
        verbose_name='Document Type'
    )
    content = models.TextField(verbose_name='Content')
    version = models.CharField(max_length=50, verbose_name='Version')
    is_active = models.BooleanField(default=False, verbose_name='Is Active')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Legal Document'
        verbose_name_plural = 'Legal Documents'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (v{self.version})"


class DocumentSignature(models.Model):
    document = models.ForeignKey(
        LegalDocument,
        on_delete=models.CASCADE,
        related_name='signatures',
        verbose_name='Document'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='document_signatures',
        verbose_name='User'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP Address'
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name='User Agent'
    )
    accepted_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Accepted At')
    is_revoked = models.BooleanField(default=False, verbose_name='Is Revoked')

    class Meta:
        verbose_name = 'Document Signature'
        verbose_name_plural = 'Document Signatures'
        unique_together = ('document', 'user')
        ordering = ['-accepted_at']

    def __str__(self):
        return f"{self.user} signed {self.document.title} (v{self.document.version})"
