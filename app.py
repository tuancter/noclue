from flask import Flask, render_template, session, redirect, url_for
from controllers.DangKyController import dangky
from controllers.DangNhapController import dangnhapnhanvien
from controllers.ThongKeChamCongController import thongkechamcong
from controllers.DangNhapAdminController import dangnhap_admin_bp 
from controllers.AdminTrangChuController import admin_bp
from controllers.timetrackController import timetrack_bp
from controllers.NhanVienTrangChuController import nhanvien_trangchu
from controllers.addFaceController import face
from controllers.faceMatchController import matching
from controllers.ThongKeLuongController import thongkeluong
from controllers.NhanVienTKLuongController import nhanvientkluong

import os

app = Flask(__name__)

app.secret_key = os.urandom(24)  # Tạo khóa bí mật ngẫu nhiên

# Đăng ký Blueprint cho các controller
app.register_blueprint(thongkechamcong, url_prefix='/thongkechamcong')  
app.register_blueprint(dangky, url_prefix='/dangky')  
app.register_blueprint(dangnhapnhanvien, url_prefix='/dangnhapnhanvien')  
app.register_blueprint(dangnhap_admin_bp, url_prefix='/trangchu')
app.register_blueprint(admin_bp, url_prefix='/admin_trangchu') 
app.register_blueprint(timetrack_bp, url_prefix='/timetrack') 
app.register_blueprint(nhanvien_trangchu, url_prefix='/nhanvien_trangchu') 
app.register_blueprint(face, url_prefix='/face')
app.register_blueprint(matching, url_prefix='/matching')
app.register_blueprint(thongkeluong, url_prefix='/thongkeluong')
app.register_blueprint(nhanvientkluong, url_prefix='/nhanvientkluong')  

@app.route('/')
def home():
    return render_template('trangchu.html')

@app.route('/logout')
def logout():
    session.pop('ma_tai_khoan', None)
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
