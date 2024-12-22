from flask import Blueprint, render_template, request, redirect, url_for
from models.NhanVien import NhanVien
from models.TaiKhoan import TaiKhoan

import hashlib

# Tạo blueprint cho đăng ký
dangky = Blueprint('dangky', __name__)

# Route đăng ký nhân viên
@dangky.route('/dangky', methods=['GET', 'POST'])
def dangky_nhanvien():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        full_name = request.form['fullName']
        birth_date = request.form['birthDate']
        address = request.form['address']
        phone_number = request.form['phoneNumber']
        email = request.form['email']
        position = request.form['position']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        ma_nhan_vien = None

        # Kiểm tra mật khẩu có trùng khớp không
        if password != confirm_password:
            message = "Mật khẩu không khớp!"
            return render_template('dangkynhanvien.html', message=message)
        #Tạo tài khoản và lưu vào cơ sở dữ liệu
        taikhoan = TaiKhoan(email, password, "nhanvien" )
        email_check_result = TaiKhoan.tao_tai_khoan(taikhoan)  # Kiểm tra email
        if email_check_result == "Email đã được sử dụng!":
            message = email_check_result
            return render_template('dangkynhanvien.html', message=message)

        else:
            TaiKhoan.tao_tai_khoan(taikhoan)
        
        #lấy mã tài khoản để lưu vào nhân viên
        ma_tai_khoan = TaiKhoan.lay_ma_tai_khoan(email)
        # Tạo đối tượng NhanVien và lưu vào cơ sở dữ liệu
        # Tạo đối tượng NhanVien và lưu vào cơ sở dữ liệu
        nhanvien = NhanVien(ma_nhan_vien, full_name, birth_date, address, phone_number, email, position, ma_tai_khoan)
        if not nhanvien.them_nhan_vien():
            message = "Email đã được sử dụng trong hệ thống!"
            return render_template('dangkynhanvien.html', message=message)

        # Thông báo đăng ký thành công
        message = "Đăng ký thành công!"
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))

    return render_template('dangkynhanvien.html')

@dangky.route('/dangnhapnhanvien', methods=['GET', 'POST'])
def dangnhap_nhanvien():
    if request.method == 'POST':
        # ...existing code...
        pass
    return render_template('dangnhapnhanvien.html')
