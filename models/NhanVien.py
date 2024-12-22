import sqlite3
from database import tao_co_so_du_lieu

class NhanVien:
    
    def __init__(self, ma_nhan_vien, ho_ten, ngay_sinh, dia_chi, so_dien_thoai, email, vi_tri, ma_tai_khoan):
        self.ma_nhan_vien = ma_nhan_vien
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.dia_chi = dia_chi
        self.so_dien_thoai = so_dien_thoai
        self.email = email
        self.vi_tri = vi_tri
        self.ma_tai_khoan = ma_tai_khoan


    def to_dict(self):
        return {
            'ho_ten': self.ho_ten,
            'ngay_sinh': self.ngay_sinh,
            'dia_chi': self.dia_chi,
            'so_dien_thoai': self.so_dien_thoai,
            'email': self.email,
            'vi_tri': self.vi_tri,

        }
    def add_nhanvien(nhanvien):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO NhanVien (ho_ten, ngay_sinh, dia_chi, so_dien_thoai, email, vi_tri, ma_tai_khoan)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nhanvien.ho_ten, nhanvien.ngay_sinh, nhanvien.dia_chi, nhanvien.so_dien_thoai, nhanvien.email, nhanvien.vi_tri, nhanvien.ma_tai_khoan))
        conn.commit()
        conn.close()

    def them_nhan_vien(self):
        # Kết nối tới cơ sở dữ liệu
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Kiểm tra xem email đã tồn tại trong bảng NhanVien chưa
        cursor.execute('''SELECT COUNT(*) FROM NhanVien WHERE email = ?''', (self.email,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return False  # Trả về False nếu email đã tồn tại

        # Chèn dữ liệu nhân viên vào bảng NhanVien
        cursor.execute('''
        INSERT INTO NhanVien (ho_ten, ngay_sinh, dia_chi, so_dien_thoai, email, vi_tri, ma_tai_khoan)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.ho_ten, self.ngay_sinh, self.dia_chi, self.so_dien_thoai, self.email, self.vi_tri, self.ma_tai_khoan))

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()

        return True  # Trả về True nếu thêm nhân viên thành công

    @staticmethod
    def lay_thong_tin_nhan_vien(ma_nhan_vien):
        """Lấy thông tin của nhân viên theo mã nhân viên."""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT ma_nhan_vien, ho_ten, ngay_sinh, dia_chi, so_dien_thoai, email, vi_tri, ma_tai_khoan
            FROM NhanVien
            WHERE ma_nhan_vien = ?
        ''', (ma_nhan_vien,))
        record = cursor.fetchone()
        connection.close()

        if record:
            # Trả về một đối tượng NhanVien với thông tin từ cơ sở dữ liệu
            nhan_vien = NhanVien(
                ma_nhan_vien = record[0],
                ho_ten=record[1],
                ngay_sinh=record[2],
                dia_chi=record[3],
                so_dien_thoai=record[4],
                email=record[5],
                vi_tri=record[6],
                ma_tai_khoan=record[7]
            )
            return nhan_vien
        else:
            return None
        
    @staticmethod
    def lay_danh_sach_nhan_vien():
        """Lấy toàn bộ danh sách nhân viên từ cơ sở dữ liệu."""
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('''
                SELECT ma_nhan_vien, ho_ten, ngay_sinh, dia_chi, so_dien_thoai, email, vi_tri, ma_tai_khoan
                FROM NhanVien
            ''')
            records = cursor.fetchall()
            connection.close()

            # Tạo danh sách các đối tượng NhanVien từ dữ liệu trả về
            danh_sach_nhan_vien = []
            for record in records:
                nhan_vien = NhanVien(
                    ma_nhan_vien=record[0],
                    ho_ten=record[1],
                    ngay_sinh=record[2],
                    dia_chi=record[3],
                    so_dien_thoai=record[4],
                    email=record[5],
                    vi_tri=record[6],
                    ma_tai_khoan=record[7]
                )
                danh_sach_nhan_vien.append(nhan_vien)
            
            return danh_sach_nhan_vien

        except sqlite3.Error as e:
            print(f"Lỗi khi lấy danh sách nhân viên: {e}")
            return []
        
    @staticmethod
    def cap_nhat_nhan_vien(ma_nhan_vien, ho_ten, ngay_sinh, vi_tri, so_dien_thoai, email, dia_chi):
        try:
            # Kết nối đến cơ sở dữ liệu SQLite
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            print("Cập nhật nhân viên với mã:", ma_nhan_vien)

            # Cập nhật dữ liệu vào bảng NhanVien
            cursor.execute('''
                UPDATE NhanVien
                SET ho_ten = ?, ngay_sinh = ?, vi_tri = ?, so_dien_thoai = ?, email = ?, dia_chi = ?
                WHERE ma_nhan_vien = ?
            ''', (ho_ten, ngay_sinh, vi_tri, so_dien_thoai, email, dia_chi, ma_nhan_vien))

            print("Cập nhật thành công!")
            
            # Lưu thay đổi và đóng kết nối
            connection.commit()
        except sqlite3.Error as e:
            print("Lỗi khi cập nhật nhân viên:", e)
        finally:
            connection.close()
    @staticmethod
    def lay_ma_nhan_vien_tu_ma_tai_khoan(ma_tai_khoan):
        # Kết nối tới cơ sở dữ liệu
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Truy vấn lấy mã nhân viên từ mã tài khoản
        cursor.execute('''SELECT ma_nhan_vien FROM NhanVien WHERE ma_tai_khoan = ?''', (ma_tai_khoan,))
        result = cursor.fetchone()

        # Đóng kết nối
        conn.close()

        # Nếu tìm thấy mã nhân viên, trả về mã nhân viên, ngược lại trả về None
        if result:
            return result[0]  # Lấy phần tử đầu tiên trong tuple (ma_nhan_vien)
        else:
            return None
        
    @staticmethod
    def xoa_nhan_vien(ma_nhan_vien):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM NhanVien WHERE ma_nhan_vien = ?', (ma_nhan_vien,))
        connection.commit()
        connection.close()
