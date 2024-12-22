from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.Luong import Luong
from models.NhanVien import NhanVien

# Tạo blueprint cho thống kê lương
thongkeluong = Blueprint('thongkeluong', __name__)

@thongkeluong.route('', methods=['GET'])
def danh_sach_nhan_vien_luong():
    # Lấy danh sách nhân viên kèm lương từ database
    danh_sach = Luong.lay_danh_sach_nhan_vien_va_luong()

    # Render dữ liệu lên giao diện
    return render_template('thongkeluong.html', danh_sach=danh_sach)

@thongkeluong.route('/search', methods=['GET'])
def search():
    thang = request.args.get('thang')
    nam = request.args.get('nam')
    search = request.args.get('search')

    # Gọi phương thức để lấy danh sách theo điều kiện
    danh_sach = Luong.lay_danh_sach_nhan_vien_va_luong(thang=thang, nam=nam, search=search)

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(danh_sach)