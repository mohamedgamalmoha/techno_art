from calendar import monthrange

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.core.validators import ValidationError
from django.contrib.auth.backends import get_user_model

from .utils import MONTHS_DICT, MONTHS_NAMES, YEARS_NUMBERS


User = get_user_model()


class Activity(models.Model):
    name = models.CharField('اسم النشاط', max_length=150)

    class Meta:
        verbose_name = 'النشاط'
        verbose_name_plural = 'النشاط'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField('اسم الموقع', max_length=150)

    class Meta:
        verbose_name = 'الموقع'
        verbose_name_plural = 'الموقع'

    def __str__(self):
        return self.name


class Month(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='العميل', related_name='user_months')
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, verbose_name='اسم النشاط')
    month = models.CharField('الشهر', max_length=150, choices=MONTHS_NAMES)
    year = models.CharField('السنة', max_length=150, choices=YEARS_NUMBERS)

    class Meta:
        verbose_name = 'الشهر'
        verbose_name_plural = 'الشهر'
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f'{self.month} of {self.user}'

    def save(self, *args, **kwargs):
        month = Month.objects.filter(user=self.user, month=self.month, year=self.year)
        if month.exists():
            raise ValidationError('invalid month')
        if not self.year:
            self.year = timezone.now().year
        return super().save(*args, **kwargs)

    def get_month_number(self):
        for month_num in MONTHS_DICT:
            if self.month in MONTHS_DICT[month_num]:
                return month_num
        return None

    def get_days_count(self):
        return monthrange(self.year, self.get_month_number())[1]

    @property
    def date(self):
        return f"{self.month} / {self.year}"


class Day(models.Model):
    month = models.ForeignKey(Month, on_delete=models.SET_NULL, null=True, verbose_name='الشهر', related_name='months')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name='الموقع')
    day_number = models.IntegerField('رقم اليوم', )
    attendance = models.BooleanField('الحضور', default=True)
    extra_work_hours = models.DecimalField('عدد سعات عمل اضافية', default=0.0,  max_digits=20, decimal_places=2)
    deduction = models.DecimalField('الخصم', default=0.0,  max_digits=20, decimal_places=2)
    rewards = models.DecimalField('المكافئات', default=0.0,  max_digits=20, decimal_places=2)
    loans = models.DecimalField('السلف', default=0.0,  max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = 'اليوم'
        verbose_name_plural = 'اليوم'

    def __str__(self):
        return f'{self.day_number}'


@receiver(models.signals.post_save, sender=Month)
def create_days_for_month(sender, instance, created, **kwargs):
    if created:
        days = instance.get_days_count()
        for day in range(days):
            Day.objects.create(month=instance, day_number=day)
