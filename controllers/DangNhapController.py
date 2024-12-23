from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.TaiKhoan import TaiKhoan
from werkzeug.security import check_password_hash

dangnhapnhanvien = Blueprint('dangnhapnhanvien', __name__)

# Route đăng nhập nhân viên
@dangnhapnhanvien.route('/dangnhapnhanvien', methods=['GET', 'POST'])
def dangnhap_nhanvien():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        tai_khoan = TaiKhoan.kiem_tra_dang_nhap(email, password)
        if tai_khoan:
            session['ma_tai_khoan'] = tai_khoan[0]
            return redirect(url_for('nhanvien_trangchu.home'))
        elif email == "admin@gmail.com" and password == "admin":
            return redirect(url_for('admin_trangchu.lay_danh_sach_nhan_vien'))
        else:
            # Nếu tài khoản hoặc mật khẩu sai
            flash("Không thể đăng nhập, vui lòng kiểm tra lại thông tin.", "danger")
            return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))  # Trở lại trang đăng nhập
       
    return render_template('dangnhapnhanvien.html')
