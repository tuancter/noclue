from flask import Blueprint, request, redirect, url_for, render_template, session, jsonify
from datetime import datetime
from models.ChamCong import ChamCong
from models.NhanVien import NhanVien
import os

timetrack_bp = Blueprint('timetrack', __name__)


@timetrack_bp.route('/')
def timetrack():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))
    else:
        id = ChamCong.getID(NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(session['ma_tai_khoan']))
        gio_ra = ChamCong.lay_thong_tin_cham_cong_theo_id(id).gio_ra
        if gio_ra == "Chưa kết thúc":
            return redirect(url_for('timetrack.endtimetrack'))
        else:
            return render_template('timetrack.html')

@timetrack_bp.route('/endtimetrack')
def endtimetrack():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))
    nhanvien = NhanVien.lay_thong_tin_nhan_vien(NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(session['ma_tai_khoan']))
    return render_template('endtimetrack.html', nhanvien = nhanvien)

@timetrack_bp.route('/time_in', methods = ['GET','POST'])
def time_in():
    try:
        id_NV = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(session["ma_tai_khoan"])
        id_CC = ChamCong.getID(id_NV)
        gio_vao = ChamCong.lay_thong_tin_cham_cong_theo_id(id_CC).gio_vao
        return jsonify({'key': gio_vao})
    except Exception as e:
        print(f"Error in time_in function: {e}")
        return e
@timetrack_bp.route('/timetrack_start', methods=['POST'])
def timetrack_create():
    data = request.get_json()
    
    requesting = data.get('requesting')
    if requesting == 'update':
        time = datetime.now()
        time_in = time.strftime("%H:%M")
        day_in = time.strftime("%Y-%m-%d")
        hour = time.hour
        minute = time.minute
        id_NV = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(session["ma_tai_khoan"])

        if (hour > 8 or (hour == 8 and minute > 10)):
            ChamCong.them_cham_cong(id_NV, day_in, time_in, "Chưa kết thúc", 'Đi muộn')
        else:
            ChamCong.them_cham_cong(id_NV, day_in, time_in, "Chưa kết thúc", 'Đi làm')
    return redirect(url_for('timetrack.endtimetrack'))
        
@timetrack_bp.route('/end', methods=['POST'])
def timetrack_end():
    time_str = request.form.get('current_time')
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    end_time = time_obj.strftime('%H:%M')
    id_NV = NhanVien.lay_ma_nhan_vien_tu_ma_tai_khoan(session["ma_tai_khoan"])
    id_CC = ChamCong.getID(id_NV)

    ChamCong.end_time(id_CC, end_time)
    return redirect(url_for('nhanvien_trangchu.home'))

@timetrack_bp.route('/filecheck', methods=['POST'])
def check_file():
    data = request.get_json()
    directory_path = os.path.join(os.getcwd(), 'uploads', 'face_registers', 'register_face.png')
    print(directory_path)
    if os.path.exists(directory_path):
        print("file exists")
        return jsonify({'exists': True})
    else:
        print("file does not exist")
        return jsonify({'exists': False})