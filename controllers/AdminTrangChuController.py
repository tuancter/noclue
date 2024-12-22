from flask import Blueprint, render_template, redirect, url_for, flash, session, jsonify, request
from models.NhanVien import NhanVien
from models.TaiKhoan import TaiKhoan
from models.ChamCong import ChamCong
from models.Luong import Luong

# Tạo Blueprint
admin_bp = Blueprint('admin_trangchu', __name__)

# Route hiển thị trang chủ admin
@admin_bp.route('/', methods=['GET', 'POST'])
def lay_danh_sach_nhan_vien():
    """Lấy danh sách nhân viên và gửi đến frontend để hiển thị."""
    try:
        danh_sach_nhan_vien = NhanVien.lay_danh_sach_nhan_vien()
        if not danh_sach_nhan_vien:
            print("không có danh sách nhân viên")
    except Exception as e:
        flash(f"Đã xảy ra lỗi khi lấy danh sách nhân viên: {str(e)}", "danger")
        print("lỗi backend")
        return redirect(url_for('thongkechamcong')) 
    
    return render_template('admin_trangchu.html', danh_sach_nhan_vien=danh_sach_nhan_vien)

# Route xem thống kê chấm công theo ID nhân viên
@admin_bp.route('/thongkechamcong/<int:id>')
def thongke_chamcong(id):
    # Chuyển hướng đến trang thống kê chấm công với ID
    return redirect(url_for('thongke.thongke_chamcong', id=id))

@admin_bp.route('/lay_thong_tin_nhan_vien/<int:ma_nhan_vien>', methods=['GET'])
def lay_thong_tin_nhan_vien(ma_nhan_vien):
    print(f"Đã nhận yêu cầu cho mã nhan vien: {ma_nhan_vien}")
    #gọi hàm để lấy thông tin chấm công theo mã chấm công
    nhan_vien_data = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
    #kiểm tra nếu không có dữ liêu
    if nhan_vien_data is None:
        return jsonify({'error': 'Không tìm thấy dữ liệu nhân viên từ back end'}), 404
    print("Nhân Viên là: ", nhan_vien_data.ho_ten)
    # Trả về dữ liệu chấm công
    return jsonify({
        'ma_nhan_vien': nhan_vien_data.ma_nhan_vien,
        'ho_ten': nhan_vien_data.ho_ten,
        'dia_chi': nhan_vien_data.dia_chi,
        'email': nhan_vien_data.email,
        'so_dien_thoai': nhan_vien_data.so_dien_thoai,
        'vi_tri': nhan_vien_data.vi_tri,
        'ngay_sinh': nhan_vien_data.ngay_sinh
    })

@admin_bp.route('/cap_nhat_nhan_vien/<int:ma_nhan_vien>', methods=['PUT'])
def cap_nhat_nhan_vien(ma_nhan_vien):
    # Lấy dữ liệu từ request
    data = request.get_json()
    ho_ten = data.get('ho_ten')
    dia_chi = data.get('dia_chi')
    vi_tri = data.get('vi_tri')
    email = data.get('email')
    ngay_sinh = data.get('ngay_sinh')
    so_dien_thoai = data.get('so_dien_thoai')

    # Cập nhật thông tin trong cơ sở dữ liệu bảng NhanVienNhanVien
    nhan_vien_data = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
    #Cập nhật thông tin trong cơ sở dữ liệu bảng TaiKhoan
    #lay ma tai khoan tu id nhân viên
    nhanvien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
    ma_tai_khoan = nhanvien.ma_tai_khoan
    #cập nhật
    TaiKhoan.cap_nhat_email(ma_tai_khoan)

    if nhan_vien_data is None:
        return jsonify({'error': 'Không tìm thấy dữ liệu chấm công từ back end'}), 404

    # Cập nhật dữ liệu vào cơ sở dữ liệu
    NhanVien.cap_nhat_nhan_vien(ma_nhan_vien, ho_ten, ngay_sinh, vi_tri, so_dien_thoai, email, dia_chi)

    return jsonify({'message': 'Cập nhật chấm công thành công'}), 200

@admin_bp.route('/xoa_nhan_vien/<int:ma_nhan_vien>', methods=['DELETE'])
def xoa_nhan_vien(ma_nhan_vien):
    print("Mã nhân viên muốn xóa là: ", ma_nhan_vien)
    try:
        nhan_vien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
        # Xóa lương liên quan đến nhân viên
        Luong.xoa_luong_theo_ma_nhan_vien(ma_nhan_vien)

        # Xóa chấm công liên quan đến nhân viên
        ChamCong.xoa_cham_cong(ma_nhan_vien)
        
        #Xóa thông tin nhân viên 
        NhanVien.xoa_nhan_vien(ma_nhan_vien)
        print("thông tin nhân viên: ", nhan_vien)

        # Xóa tài khoản liên quan đến nhân viên
        TaiKhoan.xoa_tai_khoan_theo_ma_tai_khoan(nhan_vien.ma_tai_khoan)
        # Trả về phản hồi thành công
        return jsonify({"message": "Xóa nhân viên thành công!"}), 200

    except Exception as e:
        print("Lỗi là: ", str(e))
