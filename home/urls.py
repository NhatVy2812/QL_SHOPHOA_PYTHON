from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import update_cart
from . import views # call to url_shortener/views.py
urlpatterns = [
    path('', views.home, name='home'),
    path('login/',auth_views.LoginView.as_view(template_name="page/login.html"), name="login"),
    path('sanpham/', views.sanpham_view, name='sanpham'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('contact_us/', views.about_us, name='contact_us'),
    path('my_account/', views.my_account, name='my_account'),
    path('address/', views.address, name='address'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('address/', views.address, name='address'),
    path('shop/', views.shop, name='shop'),
    path('DSSP_Loai/<int:maloai>/',views.DSSPTheoLoai, name = 'DSSPTheoLoai'),
    path('DSSP_Mau/<int:mamau>/',views.DSSPTheoMau, name = 'DSSPTheoMau'),
    path('TimKiem/',views.TimKiem, name = 'TimKiem'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thanhtoanthanhcong/', views.thanhtoanthanhcong, name='thanhtoanthanhcong'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('updatecart/', update_cart, name='update_cart'),
    path('removefromcart/', views.remove_from_cart, name='remove_from_cart'),
    path('clearcart/', views.clear_cart, name='clear_cart'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/',views.password_reset_confirm, name='password_reset_confirm'),
    path('password_change/',views.password_change, name='password_change'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    

    path('hoa_list/', views.hoa_list, name='hoa_list'),
    path('hoa_create/', views.hoa_create, name='hoa_create'),
    path('hoa_update/<int:masp>/', views.hoa_update, name='hoa_update'),
    path('hoa_delete/<int:masp>/', views.hoa_delete, name='hoa_delete'),
    path('khachhang_list/', views.khachhang_list, name='khachhang_list'),
    path('khachhang_update/<int:id>/', views.khachhang_update, name='khachhang_update'),
    path('khachhang_delete/<int:id>/', views.khachhang_delete, name='khachhang_delete'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_update/<int:id>/', views.order_update, name='order_update'),
    path('order_delete/<int:id>/', views.order_delete, name='order_delete'),
    path('quanly/', views.quanly, name='quanly'),
]
