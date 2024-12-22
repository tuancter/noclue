# DangNhapAdminController.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import NhanVien

# Tạo Blueprint cho đăng nhập admin
dangnhap_admin_bp = Blueprint('dangnhap_admin', __name__, url_prefix='/admin')

# Route đăng nhập admin
@dangnhap_admin_bp.route('/dangnhap_admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Kiểm tra thông tin đăng nhập
        if email == 'admin@gmail.com' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_trangchu.lay_danh_sach_nhan_vien'))
        else:
            flash('Email hoặc mật khẩu không đúng', 'error')
            return redirect(url_for('home'))

    return render_template('trangchu.html')

# Route trang chủ admin
@dangnhap_admin_bp.route('/admin_trangchu')
def admin_trangchu():
    return render_template('admin_trangchu.html')

@dangnhap_admin_bp.route('/trangchu')
def trangchu():
    return render_template('trangchu.html')
