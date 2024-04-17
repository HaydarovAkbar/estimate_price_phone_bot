import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

LANGUAGES = (
    ('uz', _('O\'zbek')),
    ('ru', _('Русский')),
    ('en', _('English')),
)


class User(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.BigIntegerField(verbose_name=_("Chat ID"))
    fullname = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=2, default='uz', choices=LANGUAGES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.username

    def get_fullname(self):
        return self.fullname + ' - ' + str(self.chat_id)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(User, self).save(*args, **kwargs)
        return self

    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['chat_id']),
            models.Index(fields=['created_at']),
        ]


class Channels(models.Model):
    title = models.CharField(max_length=255)
    chat_id = models.BigIntegerField(null=True)
    url = models.URLField(null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Channels, self).save(*args, **kwargs)
        return self

    class Meta:
        db_table = 'channels'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Nomi"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Narxi"))
    description = models.TextField(verbose_name=_("Tavsif"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Product, self).save(*args, **kwargs)
        return self

    class Meta:
        db_table = 'product'
