# Generated by Django 5.0.4 on 2024-05-30 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_sanpham_mamau'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanpham',
            name='MaMau',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.mausac'),
        ),
    ]