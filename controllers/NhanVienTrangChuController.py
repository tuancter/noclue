from flask import render_template, redirect, url_for, flash, request, session
from models.TaiKhoan import TaiKhoan
from models.ChamCong import ChamCong
from models.NhanVien import NhanVien
from flask import Blueprint

# Tạo Blueprint cho trang chủ nhân viên
nhanvien_trangchu = Blueprint('nhanvien_trangchu', __name__)

@nhanvien_trangchu.route('/', methods=['GET', 'POST'])
def home():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))
    else:
        ma_tai_khoan = session['ma_tai_khoan']
        ma_nhan_vien = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(ma_tai_khoan)
        nhan_vien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
        danh_sach_cham_cong = ChamCong.lay_danh_sach_cham_cong(ma_nhan_vien)
        print("danh_sach_cham_cong: ", danh_sach_cham_cong)
        return render_template('nhanvientrangchu.html', nhan_vien=nhan_vien, danh_sach_cham_cong=danh_sach_cham_cong)

@nhanvien_trangchu.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))
    else:
        ma_tai_khoan = session['ma_tai_khoan']
        ma_nhan_vien = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(ma_tai_khoan)
        nhan_vien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
        return render_template('profile.html', nhan_vien=nhan_vien)
    
@nhanvien_trangchu.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhan_vien'))
    else:
        ma_tai_khoan = session['ma_tai_khoan']
        ma_nhan_vien = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(ma_tai_khoan)
        nhan_vien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
        if request.method == 'POST':
            data = request.get_json()
            ho_ten = data.get('ho_ten')
            ngay_sinh = data.get('ngay_sinh')
            dia_chi = data.get('dia_chi')
            so_dien_thoai = data.get('so_dien_thoai')
            email = data.get('email')
            vi_tri = data.get('vi_tri')
            NhanVien.cap_nhat_nhan_vien(ma_nhan_vien, ho_ten, ngay_sinh, vi_tri, so_dien_thoai, email, dia_chi);
            return 'success', 204
        return render_template('edit.html', nhan_vien=nhan_vien)
