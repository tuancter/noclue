
import sqlite3

def tao_co_so_du_lieu():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tạo bảng TaiKhoan
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TaiKhoan (
        ma_tai_khoan INTEGER PRIMARY KEY AUTOINCREMENT,
        email_dang_nhap TEXT UNIQUE NOT NULL,
        mat_khau TEXT NOT NULL,
        quyen TEXT CHECK(quyen IN ('admin', 'nhanvien')) NOT NULL
    )
    ''')

    # Tạo bảng NhanVien
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NhanVien (
        ma_nhan_vien INTEGER PRIMARY KEY AUTOINCREMENT,
        ho_ten TEXT NOT NULL,
        ngay_sinh DATE NOT NULL,
        dia_chi TEXT NOT NULL,
        so_dien_thoai TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        vi_tri TEXT NOT NULL,
        ma_tai_khoan INTEGER NOT NULL,
        FOREIGN KEY (ma_tai_khoan) REFERENCES TaiKhoan(ma_tai_khoan)
    )
    ''')

    # Tạo bảng ChamCong
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChamCong (
        ma_cham_cong INTEGER PRIMARY KEY AUTOINCREMENT,
        ma_nhan_vien INTEGER NOT NULL,
        ngay DATE NOT NULL,
        gio_vao TIME,
        gio_ra TIME,
        phuong_thuc TEXT CHECK(phuong_thuc IN ('Nhận diện', 'Thủ công')) NOT NULL,
        trang_thai TEXT CHECK(trang_thai IN ('Đi làm', 'Đi muộn', 'Không đi làm')) NOT NULL,
        FOREIGN KEY (ma_nhan_vien) REFERENCES NhanVien(ma_nhan_vien)

    )
    ''')

# Tạo bảng Luong
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Luong (
        ma_luong INTEGER PRIMARY KEY AUTOINCREMENT,
        ma_nhan_vien INTEGER NOT NULL,
        thang TEXT NOT NULL,
        nam TEXT NOT NULL,
        so_ngay_di_lam INTEGER NOT NULL,
        so_ngay_di_muon INTEGER NOT NULL,
        tong_luong REAL NOT NULL,
        FOREIGN KEY (ma_nhan_vien) REFERENCES NhanVien(ma_nhan_vien),
        UNIQUE(ma_nhan_vien, thang, nam)  -- Thêm ràng buộc duy nhất cho ma_nhan_vien, thang, nam
    )
    ''')


    conn.commit()
    conn.close()

# Gọi hàm để tạo cơ sở dữ liệu
tao_co_so_du_lieu()
