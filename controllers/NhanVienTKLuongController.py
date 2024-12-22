from flask import render_template, redirect, url_for, flash, request, session
from models.TaiKhoan import TaiKhoan
from models.ChamCong import ChamCong
from models.NhanVien import NhanVien
from models.Luong import Luong
from flask import Blueprint

# Tạo blueprint cho nhân viên thống kê lươnglương
nhanvientkluong = Blueprint('nhanvientkluong', __name__)

# Route để hiển thị thống kê lương của nhân viên
@nhanvientkluong.route('/', methods=['GET'])
def hien_thi_thong_ke_luong():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))
    try:
        ma_tai_khoan = session.get('ma_tai_khoan')  # Giả sử mã tài khoản được lưu trong session
        print("Mã tài khoản là: ", ma_tai_khoan)
        ma_nhan_vien = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(ma_tai_khoan)
        print("Mã nhân viên là: ", ma_nhan_vien)
        # Lấy danh sách lương của nhân viên
        Luong.tong_hop_luong_cuoi_thang(ma_nhan_vien)
        danh_sach_luong = Luong.get_luong_by_nhanvien_id(ma_nhan_vien)

        # Lấy thông tin nhân viên
        thong_tin_nhan_vien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)

        # Kiểm tra nếu danh sách lương trống
        if not danh_sach_luong:
            print("Không tìm thấy danh sách lương cho nhân viên này")

        print(danh_sach_luong)
        print(thong_tin_nhan_vien)

    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")
        return redirect(url_for('dangkynhanvien'))

    return render_template(
        'nhanvien_xemluong.html',
        danh_sach_luong=danh_sach_luong,
        thong_tin_nhan_vien=thong_tin_nhan_vien,
        ma_nhan_vien=ma_nhan_vien
    )