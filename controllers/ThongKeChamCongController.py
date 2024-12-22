from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.ChamCong import ChamCong
from models.NhanVien import NhanVien



# Tạo blueprint cho thống kê chấm công
thongkechamcong = Blueprint('thongkechamcong', __name__)

# Route để hiển thị thống kê chấm công của nhân viên
@thongkechamcong.route('/<int:ma_nhan_vien>', methods=['GET'])
def hien_thi_thong_ke(ma_nhan_vien):
    print("Mã nhân viên là: dddddddddddddddddddddd ", ma_nhan_vien)
    try:
        danh_sach_cham_cong = ChamCong.lay_danh_sach_cham_cong(ma_nhan_vien)
        thong_tin_nhan_vien = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
        print(danh_sach_cham_cong)
        print(thong_tin_nhan_vien)
    except Exception as e:
        flash(f"Có lỗi xảy ra: {str(e)}", "danger")
        return redirect(url_for('dangkynhanvien'))
        
    return render_template('thongkechamcong.html', danh_sach_cham_cong=danh_sach_cham_cong, thong_tin_nhan_vien=thong_tin_nhan_vien, ma_nhan_vien = ma_nhan_vien)


@thongkechamcong.route('thongkechamcong/lay_thong_tin_cham_cong/<int:ma_cham_cong>', methods=['GET'])
def lay_thong_tin_cham_cong(ma_cham_cong):
    print(f"Đã nhận yêu cầu cho mã chấm công: {ma_cham_cong}")
    #gọi hàm để lấy thông tin chấm công theo mã chấm công
    cham_cong_data = ChamCong.lay_thong_tin_cham_cong_theo_id(ma_cham_cong)
    #kiểm tra nếu không có dữ liêu
    if cham_cong_data is None:
        return jsonify({'error': 'Không tìm thấy dữ liệu chấm công từ back end'}), 404

    # Trả về dữ liệu chấm công
    return jsonify({
        'status': cham_cong_data['trang_thai'],  # 'trang_thai'
        'start_time': cham_cong_data['gio_vao'],  # 'gio_vao'
        'end_time': cham_cong_data['gio_ra']     # 'gio_ra'
    })




@thongkechamcong.route('thongkechamcong/cap_nhat_cham_cong/<int:ma_cham_cong>', methods=['PUT'])
def cap_nhat_cham_cong(ma_cham_cong):
    # Lấy dữ liệu từ request
    data = request.get_json()
    status = data.get('status')
    print("trạng thái là: ", status)
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    # Cập nhật thông tin trong cơ sở dữ liệu
    cham_cong_data = ChamCong.lay_thong_tin_cham_cong_theo_id(ma_cham_cong)

    if cham_cong_data is None:
        return jsonify({'error': 'Không tìm thấy dữ liệu chấm công từ back end'}), 404

    # Cập nhật dữ liệu vào cơ sở dữ liệu
    ChamCong.cap_nhat_cham_cong(ma_cham_cong, status, start_time, end_time)

    return jsonify({'message': 'Cập nhật chấm công thành công'}), 200
