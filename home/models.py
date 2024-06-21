from django.db import models

from django.contrib.auth.models import User
# Create your models here
STATUS_CHOICES=(
     ('Chờ xác nhận','Chờ xác nhận'),
     ('Đang giao hàng','Đang giao hàng'),
     ('Hủy đơn hàng','Hủy đơn hàng'),
     ('Giao thành công','Giao thành công'),
     
)        
class Loai(models.Model):
    MaLoai = models.AutoField(primary_key=True)
    TenLoai = models.CharField(max_length=100)
    def __str__(self):
            return self.TenLoai
class MauSac(models.Model):
    MaMau = models.AutoField(primary_key=True)
    TenMau = models.CharField(max_length=100)
    def __str__(self):
            return self.TenMau
class SanPham(models.Model):
    MaSP = models.AutoField(primary_key=True)
    TenSP = models.CharField(max_length=255)
    MoTa = models.CharField(max_length=500)
    SoLuong = models.PositiveIntegerField()
    DonGia = models.DecimalField(max_digits=10, decimal_places=2)
    HinhAnh = models.ImageField(upload_to='product')
    MaLoai = models.ForeignKey(Loai, on_delete=models.CASCADE)
    MaMau = models.ForeignKey(MauSac, on_delete=models.SET_NULL, null =True)
    def __str__(self):
        return self.TenSP
class KhachHang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TenKH = models.CharField(max_length=200)
    DiaChi = models.CharField(max_length=400)
    DienThoai = models.IntegerField(default=0)
    def __str__(self):
        return self.TenKH

class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     sanpham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
     soluong = models.PositiveIntegerField(default=1)
     @property
     def tong_tien(self):
        return self.soluong * self.sanpham.DonGia
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    khachhang = models.ForeignKey(KhachHang,on_delete=models.CASCADE)
    sanpham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    soluong = models.PositiveIntegerField(default=1)
    ngaydat = models.DateTimeField(auto_now_add=True)
    tinhtrang = models.CharField(max_length=100,choices=STATUS_CHOICES,default='Chờ xác nhận')
    @property
    def tong_tien(self):
         return self.soluong * self.sanpham.DonGia 