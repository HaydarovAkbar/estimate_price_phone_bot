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
        try:
            return self.fullname + ' - ' + str(self.chat_id)
        except Exception:
            return str(self.id) + ' - ' + str(self.chat_id)

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

    abstract = True


class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Nomi"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Categories, self).save(*args, **kwargs)
        return self

    abstract = True


class Capacities(models.Model):
    """Емкости"""
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Capacities, self).save(*args, **kwargs)
        return self

    abstract = True


class Colors(models.Model):
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Colors, self).save(*args, **kwargs)
        return self

    abstract = True


class Memories(models.Model):
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Memories, self).save(*args, **kwargs)
        return self

    abstract = True


class Documents(models.Model):
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Documents, self).save(*args, **kwargs)
        return self

    abstract = True


class Countries(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=25, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Countries, self).save(*args, **kwargs)
        return self

    abstract = True


class Statuses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Statuses, self).save(*args, **kwargs)
        return self

    abstract = True


class Prices(models.Model):
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Prices, self).save(*args, **kwargs)
        return self

    abstract = True


class Products(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Nomi"))
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    hashtags = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(Products, self).save(*args, **kwargs)
        return self

    abstract = True


class ProductCriteria(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='criteria')
    capacity = models.ForeignKey(Capacities, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, null=True, blank=True)
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE, null=True, blank=True)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.product.title

    abstract = True
