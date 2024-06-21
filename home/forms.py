from django import forms
import re
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import KhachHang

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Tên', max_length=30)
    last_name = forms.CharField(label='Họ', max_length=30)
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']

            if len(password1) < 8:
                raise forms.ValidationError("Mật khẩu phải có ít nhất 8 ký tự")
            
            if not re.search(r'\d', password1):
                raise forms.ValidationError("Mật khẩu phải chứa ít nhất một số")
            
            if password1 != password2:
                raise forms.ValidationError("Mật khẩu không hợp lệ")
            
            return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tài khoản đã tồn tại")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'], 
            email=self.cleaned_data['email'], 
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        if commit:
            user.save()
        return user

class ThongTinKhachHang(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields=['TenKH','DiaChi','DienThoai']
        widgets={
            'TenKH':forms.TextInput(attrs={'class':'single-input-item mb-2'}),
            'DiaChi':forms.TextInput(attrs={'class':'single-input-item mb-2'}),
            'DienThoai':forms.TextInput(attrs={'class':'single-input-item mb-2'}),
        }
        labels = {
            'TenKH': 'Tên Khách Hàng',
            'DiaChi': 'Địa Chỉ',
            'DienThoai': 'Điện Thoại',
        }

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1','new_password2']
class PasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super(PasswordResetForm, self).__init__(*args,**kwargs)