from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import SanPham, Loai, MauSac,KhachHang,Cart,Order
from .forms import RegistrationForm, ThongTinKhachHang
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect 
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q

from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from django.contrib.auth.tokens import default_token_generator

account_activation_token = default_token_generator

from .tokens import account_activation_token

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Tài khoản {user.username} đã được kích hoạt')
        return redirect('login')
    else:
        messages.error(request, 'Lỗi kích hoạt tài khoản')
        return redirect('register')

def activateEmail(request, user, to_email):
    mail_subject = "Xác minh Email"
    message = render_to_string('page/activate_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Gửi  {user.username}, please go to your email {to_email}')
    else:
        messages.error(request, f'Lỗi gửi tới {to_email}')


def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        
        # Lấy thông tin sản phẩm từ cơ sở dữ liệu
        cart_item = Cart.objects.get(id=item_id)
        cart_item.soluong = quantity
        cart_item.save()
        
        # Lấy lại thông tin sản phẩm sau khi cập nhật số lượng
        cart_item.refresh_from_db()
        tong_tien = cart_item.soluong * cart_item.sanpham.DonGia
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.sanpham.DonGia * item.soluong for item in cart_items)
        # Trả về dữ liệu cập nhật dưới dạng JSON
        data = {
            'quantity': quantity,
            'total_amount': total_amount,  # Sử dụng thuộc tính tính toán tong_tien
            'tong_tien': tong_tien
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request'})

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        try:
            # Tìm kiếm và xóa sản phẩm từ giỏ hàng
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()

            # Tính toán lại tổng số tiền
            cart_items = Cart.objects.filter(user=request.user)
            total_amount = sum(item.sanpham.DonGia * item.soluong for item in cart_items)

            # Trả về dữ liệu cập nhật cho giao diện
            return JsonResponse({'total_amount': total_amount})

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Sản phẩm không tồn tại'}, status=400)

    return JsonResponse({'error': 'Phương thức không hợp lệ'}, status=405)
def clear_cart(request):
    if request.method == 'POST':
        try:
            # Xóa tất cả các sản phẩm trong giỏ hàng
            Cart.objects.filter(user=request.user).delete()

            # Tính toán lại tổng số tiền
            total_amount = 0

            # Trả về dữ liệu cập nhật cho giao diện
            return JsonResponse({'total_amount': total_amount})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không hợp lệ'}, status=405)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'page/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    data={
            'item_sanpham': SanPham.objects.all(),
            'item_loai': Loai.objects.all(),
    }
    return render(request, 'page/home.html',data)
def DSSPTheoLoai(request, maloai):
  
    dssp = SanPham.objects.filter(MaLoai = maloai)
    data = {
        
        'dm_sanpham': dssp,
        'item_sanpham': SanPham.objects.all(),
        'item_loai': Loai.objects.all(),
    }
    return render(request, 'page/shop1.html', data)
def DSSPTheoMau(request, mamau):
  
    dssp = SanPham.objects.filter(MaMau = mamau)
    data = {
        
        'dm_sanpham': dssp,
        'item_sanpham': SanPham.objects.all(),
        'item_loai': Loai.objects.all(),
        'item_mausac': MauSac.objects.all(),
    }
    return render(request, 'page/shop2.html', data)
def TimKiem(request):
    keyword = request.POST.get('keyword', '')
    dssp = SanPham.objects.filter(TenSP__icontains=keyword)
    data = {
        
        'dm_sanpham': dssp,
        'item_sanpham': SanPham.objects.all(),
        'item_loai': Loai.objects.all(),
        'item_mausac': MauSac.objects.all(),
    }
    return render(request, 'page/shop3.html', data)
def login(request):
    return render(request, 'page/login.html')


def about_us(request):
    return render(request, 'page/contact_us.html')

def shop(request):
    data={
            'item_sanpham': SanPham.objects.all(),
            'item_loai': Loai.objects.all(),
            'item_mausac': MauSac.objects.all(),
    }
    return render(request, 'page/shop.html',data)

def cart(request):
    return render(request, 'page/cart.html')

def checkout(request):
    add = KhachHang.objects.filter(user=request.user)
    cart = Cart.objects.filter(user = request.user)
    total_price = sum(item.tong_tien for item in cart)
    return render(request, 'page/checkout.html',{'cart': cart, 'tong': total_price,'add':add})

def sanpham_view(request):
    sanpham_list = SanPham.objects.all().order_by('DonGia')
    return render(request, 'page/shop1.html', {'sanpham_list': sanpham_list})

def my_account(request):
    user = request.user

    if request.method == 'POST':
        form = ThongTinKhachHang(request.POST)
        if form.is_valid():
            TenKH = form.cleaned_data['TenKH']
            DiaChi = form.cleaned_data['DiaChi']
            DienThoai = form.cleaned_data['DienThoai']

            KhachHang.objects.create(user=user, TenKH=TenKH, DiaChi=DiaChi, DienThoai=DienThoai)
            messages.success(request, "Thêm thông tin thành công")
            return redirect('home')  # Redirect to home after successful update
        else:
            messages.warning(request, "Không có giá trị dữ liệu")
    else:
        form = ThongTinKhachHang()

    return render(request, 'page/my_account.html', {'form': form})
   
def address(request):
    add = KhachHang.objects.filter(user=request.user)
    return render(request,'page/address.html',locals())
def update_profile(request):
    
    return render(request, 'update_profile.html')


def forgot_password(request):
    return render(request, 'page/forgot_password.html')


def product_details(request, product_id):
    sp = SanPham.objects.get(MaSP = product_id)
    data = {
        'sanpham':sp,
        'item_sanpham': SanPham.objects.all(),
        'item_loai': Loai.objects.all(),
    }
    return render(request, 'page/product_details.html',data)


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    sanpham = SanPham.objects.get(MaSP=product_id)
    quantity = int(request.GET.get('soluong'))
    # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng hay chưa
    existing_cart_item = Cart.objects.filter(user=user, sanpham=sanpham).first()

    if existing_cart_item:
        # Nếu sản phẩm đã tồn tại trong giỏ hàng, cập nhật số lượng
        existing_cart_item.soluong += quantity
        existing_cart_item.save()
    else:
        # Nếu sản phẩm chưa có trong giỏ hàng, tạo một mục mới
        Cart(user=user, sanpham=sanpham, soluong = quantity).save()

    return redirect("/cart")
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    total_price = sum(item.tong_tien for item in cart)
    item_loai=Loai.objects.all()
    return render(request,'page/addtocart.html',{'cart': cart, 'tong': total_price,'item_loai':item_loai})
def thanhtoanthanhcong(request):
    user = request.user
    cust_id=request.GET.get('custid')
    khachhang = KhachHang.objects.get(id = cust_id )
    cart = Cart.objects.filter(user=request.user)
    for c in cart:
        Order(user = user,khachhang = khachhang, sanpham = c.sanpham, soluong = c.soluong).save()
        c.delete()
    return render(request, 'page/thankyou.html')
   

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SetPasswordForm(user)
    return render(request, 'page/password_reset_confirm.html', {'form': form})
   
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Yêu cầu đổi mật khẩu"
                message = render_to_string("page/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, "Vui lòng kiểm tra hộp thư email")
                else:
                    messages.error(request, "Problem sending reset password email")
            else:
                messages.error(request, "No user is associated with this email address")
            return redirect('password_reset')
    else:
        form = PasswordResetForm()
    return render(request, 'page/password_reset.html', {'form': form})
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Tài khoản {user.username} đã đặt được mật khẩu mới.')
                return redirect('login')
            else:
                messages.error(request, 'Lỗi khi đặt mật khẩu mới. Vui lòng thử lại.')
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, 'Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.')
        form = None

    return render(request, 'page/password_reset_confirm.html', {'form': form})
            
def hoa_list(request):
    item_sanpham = SanPham.objects.all()
    return render(request, 'QuanLy/hoa_list.html',{'item_sanpham':item_sanpham})
def hoa_create(request):
    if request.method == "POST":
        TenSP = request.POST.get('TenSP')
        DonGia = request.POST.get('DonGia')
        MoTa = request.POST.get('MoTa')
        HinhAnh = request.FILES.get('HinhAnh')  # Lấy hình ảnh từ request.FILES
        SoLuong = request.POST.get('SoLuong')
        MaMau = request.POST.get('MaMau')
        MaLoai = request.POST.get('MaLoai')

        # Lấy đối tượng MaLoai và MaMau từ cơ sở dữ liệu
        MaLoai = Loai.objects.get(MaLoai = MaLoai)
        MaMau = MauSac.objects.get(MaMau = MaMau)

        item_sanpham = SanPham(
            TenSP=TenSP, 
            MoTa=MoTa, 
            SoLuong=SoLuong, 
            DonGia=DonGia, 
            HinhAnh=HinhAnh, 
            MaLoai=MaLoai, 
            MaMau=MaMau
        )
        item_sanpham.save()

        return redirect('hoa_list')
    
    loai_list = Loai.objects.all()  # Lấy tất cả các loại để hiển thị trong dropdown
    mausac_list = MauSac.objects.all()  # Lấy tất cả các màu để hiển thị trong dropdown
    return render(request, 'QuanLy/hoa_create.html', {
        'loai_list': loai_list,
        'mausac_list': mausac_list
    })
def hoa_update(request, masp):
    item_sanpham = SanPham.objects.get(MaSP = masp)
    if request.method == "POST":
        TenSP = request.POST.get('TenSP')
        DonGia = request.POST.get('DonGia')
        MoTa = request.POST.get('MoTa')
        HinhAnh = request.FILES.get('HinhAnh')  # Lấy hình ảnh từ request.FILES
        SoLuong = request.POST.get('SoLuong')
        MaMau = request.POST.get('MaMau')
        MaLoai = request.POST.get('MaLoai')

        # Lấy đối tượng MaLoai và MaMau từ cơ sở dữ liệu
        MaLoai = Loai.objects.get(MaLoai = MaLoai)
        MaMau = MauSac.objects.get(MaMau = MaMau)

        item_sanpham.TenSP = TenSP
        item_sanpham.DonGia = DonGia
        item_sanpham.MoTa = MoTa
        if HinhAnh:
            item_sanpham.HinhAnh = HinhAnh
        item_sanpham.SoLuong = SoLuong
        item_sanpham.MaLoai = MaLoai
        item_sanpham.MaMau = MaMau
        item_sanpham.save()

        return redirect('hoa_list')
    
    loai_list = Loai.objects.all()  # Lấy tất cả các loại để hiển thị trong dropdown
    mausac_list = MauSac.objects.all()  # Lấy tất cả các màu để hiển thị trong dropdown
    return render(request, 'QuanLy/hoa_update.html', {
        'loai_list': loai_list,
        'mausac_list': mausac_list,
        'item_sanpham':item_sanpham
    })
def hoa_delete(request, masp):
    item_sanpham = SanPham.objects.get(MaSP = masp)
    item_sanpham.delete()
    return redirect('hoa_list')
def khachhang_list(request):
    item_khachhang = KhachHang.objects.all()
    return render(request, 'QuanLy/khachhang_list.html',{'item_khachhang':item_khachhang})
def khachhang_update(request, id):
    item_khachhang = KhachHang.objects.get(id = id)
    if request.method == "POST":
        user = request.POST.get('user')
        TenKH = request.POST.get('TenKH')
        DiaChi = request.POST.get('DiaChi')
        DienThoai = request.POST.get('DienThoai')
      


        item_khachhang.user = user
        item_khachhang.TenKH = TenKH
        item_khachhang.DiaChi = DiaChi
        item_khachhang.DienThoai = DienThoai
        item_khachhang.user = request.user
        item_khachhang.save()

        return redirect('khachhang_list')
    return render(request, 'QuanLy/khachhang_update.html', {'item_khachhang':item_khachhang})
def khachhang_delete(request, id):
    item_khachhang = KhachHang.objects.get(id = id)
    item_khachhang.delete()
    return redirect('khachhang_list')
def order_update(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        khachhang =  KhachHang.objects.get(id=request.POST.get('khachhang'))
        sanpham = SanPham.objects.get(MaSP=request.POST.get('sanpham'))
        soluong = request.POST.get('soluong')
        tinhtrang = request.POST.get('tinhtrang')

        order.khachhang = khachhang
        order.sanpham = sanpham
        order.soluong = soluong
        order.tinhtrang = tinhtrang
        order.save()

        order.save()
        return redirect('order_list')

    khachhang_list = KhachHang.objects.all()
    sanpham_list = SanPham.objects.all()
    return render(request, 'QuanLy/hoadon_update.html', {'order': order, 'khachhang_list': khachhang_list, 'sanpham_list': sanpham_list})

# View to delete an order
def order_delete(request, id):
    order =  Order.objects.get(id=id)
    order.delete()
    return redirect('order_list')

# View to list all orders
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'QuanLy/hoadon_list.html', {'orders': orders})   
def quanly(request):
    return render(request, 'QuanLy/quanly.html')   