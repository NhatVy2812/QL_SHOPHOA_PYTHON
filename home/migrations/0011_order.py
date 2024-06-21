# Generated by Django 5.0.4 on 2024-06-02 09:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soluong', models.PositiveIntegerField(default=1)),
                ('ngaydat', models.DateTimeField(auto_now_add=True)),
                ('tinhtrang', models.CharField(choices=[('Chờ xác nhận', 'Chờ xác nhận'), ('Đang giao hàng', 'Đang giao hàng'), ('Hủy đơn hàng', 'Hủy đơn hàng'), ('Giao thành công', 'Giao thành công')], default='Chờ xác nhận', max_length=100)),
                ('khachhang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.khachhang')),
                ('sanpham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sanpham')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
