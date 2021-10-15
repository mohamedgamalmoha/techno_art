# Generated by Django 3.2.8 on 2021-10-14 22:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('affairs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='year',
            field=models.CharField(choices=[(2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)], max_length=150, verbose_name='السنة'),
        ),
        migrations.AlterUniqueTogether(
            name='month',
            unique_together={('user', 'month', 'year')},
        ),
    ]