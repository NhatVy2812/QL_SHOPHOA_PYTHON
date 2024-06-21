from django.contrib import admin
from .models import SanPham, Loai,MauSac, KhachHang, Cart,Order
# Register your models here.
@admin.register(SanPham)
class SanPhamModelAdmin(admin.ModelAdmin):
    list_display = ['MaSP','TenSP','DonGia','SoLuong','MaLoai','HinhAnh']
@admin.register(Loai)
class LoaiModelAdmin(admin.ModelAdmin):
    list_display = ['MaLoai','TenLoai']
@admin.register(MauSac)
class MauSacModelAdmin(admin.ModelAdmin):
    list_display = ['MaMau','TenMau']
@admin.register(KhachHang)
class KhachHangModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','TenKH','DiaChi','DienThoai']
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','sanpham','soluong']
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','khachhang','sanpham','ngaydat','tinhtrang']