# Generated by Django 4.0.5 on 2022-06-16 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
                ('introduction', models.TextField(verbose_name='소개')),
                ('birthday', models.DateField(verbose_name='생일')),
                ('age', models.IntegerField(verbose_name='나이')),
            ],
        ),
    ]
