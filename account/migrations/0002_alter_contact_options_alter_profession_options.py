# Generated by Django 4.0.6 on 2022-08-22 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
        migrations.AlterModelOptions(
            name='profession',
            options={'verbose_name': 'Профессия', 'verbose_name_plural': 'Профессии'},
        ),
    ]
