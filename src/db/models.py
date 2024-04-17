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


class Organization(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("To'liq nomi"))

    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Manzil"))
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Telefon"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Tavsif"))
    leader = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Rahbar"))

    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan sana"))

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper() if self.title else self.title
        self.updated_at = now()
        super(Organization, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Tashkilotlar')
        verbose_name = _('Tashkilot')
        db_table = 'organization'


class PaymentType(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("To'liq nomi"))

    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("O'zgartirilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper() if self.title else self.title
        self.updated_at = now()
        super(PaymentType, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('To\'lov turlari')
        verbose_name = _('To\'lov turi')
        db_table = 'payment_type'


class FuelType(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("To'liq nomi"))
    attr = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Qisqa nomi"))

    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("O'zgartirilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper() if self.title else self.title
        self.updated_at = now()
        super(FuelType, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Yoqilg\'i turlari')
        verbose_name = _('Yoqilg\'i turi')
        db_table = 'fuel_type'


class FuelColumn(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("To'liq nomi"))

    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("O'zgartirilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper() if self.title else self.title
        self.updated_at = now()
        super(FuelColumn, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Yoqilg\'i ustunlari')
        verbose_name = _('Yoqilg\'i ustuni')
        db_table = 'fuel_column'


class FuelStorage(models.Model):
    remainder = models.IntegerField(verbose_name=_("Kirim Hajmi [litr]"))
    residual = models.IntegerField(verbose_name=_("Qoldiq [litr]"))
    price = models.FloatField(verbose_name=_("Kirim narxi"))
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))
    is_over = models.BooleanField(default=False, verbose_name=_("Tugaganmi"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("O'zgartirilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return str(self.remainder)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(FuelStorage, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Yoqilg\'i ombori')
        verbose_name = _('Yoqilg\'i ombori')
        db_table = 'fuel_storage'


class FuelColumnPointer(models.Model):
    fuel_column = models.ForeignKey(FuelColumn, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i ustuni"))
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))
    size_first = models.FloatField(verbose_name=_("Hajmi kun boshida [litr]"), null=True, blank=True)
    size_last = models.FloatField(verbose_name=_("Hajmi kun oxirida [litr]"), null=True, blank=True)
    organ = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return str(self.size_first)

    def save(self, *args, **kwargs):
        super(FuelColumnPointer, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Yoqilg\'i ustuni ko\'rsatgichlari')
        verbose_name = _('Yoqilg\'i ustuni ko\'rsatgichlari')
        db_table = 'fuel_column_pointer'


class User(models.Model):
    username = models.CharField(max_length=255, verbose_name=_("Foydalanuvchi nomi"), null=True, blank=True)
    chat_id = models.BigIntegerField(verbose_name=_("Chat ID"))
    fullname = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("To'liq ismi"))
    language = models.CharField(max_length=2, default='uz', verbose_name=_("Til"), choices=LANGUAGES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    phone = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)
    is_cashier = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.username

    def get_fullname(self):
        return self.fullname + ' - ' + str(self.chat_id)

    def get_user(self):
        try:
            return self.fullname + ' - ' + str(self.created_at.strftime('%d-%m-%Y %H:%M'))
        except:
            return str(self.chat_id) + ' - ' + str(self.created_at.strftime('%d-%m-%Y %H:%M'))

    def check_admin(self):
        if self.is_admin:
            return True
        return False

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(User, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Foydalanuvchilar')
        verbose_name = _('Foydalanuvchi')
        db_table = 'user'


class SaleFuel(models.Model):
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))
    price = models.FloatField(verbose_name=_("Narxi"), null=True, blank=True)
    benefit = models.FloatField(null=True, blank=True)

    cash_size = models.FloatField(verbose_name=_("Naxt hajmi [litr]"), null=True, blank=True)
    card_size = models.FloatField(verbose_name=_("Plastig hajmi [litr]"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("O'zgartirilgan sana"))

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))

    objects = models.Manager()

    def __str__(self):
        return str(self.created_at)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(SaleFuel, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Sotilgan yoqilg\'i')
        verbose_name = _('Sotilgan yoqilg\'i')
        db_table = 'sale_fuel'
        indexes = [
            models.Index(fields=['fuel_type']),
        ]


class OrganizationFuelColumns(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))
    fuel_column = models.ForeignKey(FuelColumn, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i ustuni"))
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return str(self.organization)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(OrganizationFuelColumns, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Tashkilotlar yoqilg\'i ustunlari')
        verbose_name = _('Tashkilotlar yoqilg\'i ustuni')
        db_table = 'organization_fuel_columns'


class OrganizationFuelTypes(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return str(self.organization)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(OrganizationFuelTypes, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Tashkilotlar yoqilg\'i turlari')
        verbose_name = _('Tashkilotlar yoqilg\'i turi')
        db_table = 'organization_fuel_types'


class FuelPrice(models.Model):
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))
    price = models.FloatField(verbose_name=_("Narxi"))
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("O'zgartirilgan sana"))

    objects = models.Manager()

    def __str__(self):
        return str(self.price)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super(FuelPrice, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Yoqilg\'i narxlari')
        verbose_name = _('Yoqilg\'i narxi')
        db_table = 'fuel_price'
        indexes = [
            models.Index(fields=['fuel_type']),
        ]


class FuelStorageHistory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name=_("Tashkilot"))
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True, verbose_name=_("Yoqilg'i turi"))

    created_at = models.DateTimeField(auto_now_add=True)

    begin = models.IntegerField(verbose_name=_("Kun boshida [litr]"))
    end = models.IntegerField(verbose_name=_("Kun oxirida [litr]"))

    objects = models.Manager()

    def __str__(self):
        return str(self.begin)

    def save(self, *args, **kwargs):
        super(FuelStorageHistory, self).save(*args, **kwargs)
        return self

    class Meta:
        verbose_name_plural = _('Yoqilg\'i ombori tarixi')
        verbose_name = _('Yoqilg\'i ombori tarixi')
        db_table = 'fuel_storage_history'
