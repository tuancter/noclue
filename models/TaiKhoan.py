import sqlite3
import hashlib
from database import tao_co_so_du_lieu

class TaiKhoan:
    def __init__(self, email_dang_nhap, mat_khau, quyen):
        self.email_dang_nhap = email_dang_nhap
        self.mat_khau = mat_khau
        self.quyen = quyen

    def tao_tai_khoan(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Kiểm tra xem email đã tồn tại trong cơ sở dữ liệu chưa
        cursor.execute('''SELECT email_dang_nhap FROM TaiKhoan WHERE email_dang_nhap = ?''', (self.email_dang_nhap,))
        existing_email = cursor.fetchone()

        if existing_email:  # Nếu email đã tồn tại
            conn.close()
            return False  # Trả về False khi email đã tồn tại

        # Mã hóa mật khẩu
        hashed_password = hashlib.sha256(self.mat_khau.encode()).hexdigest()

        # Thêm tài khoản vào bảng TaiKhoan
        cursor.execute('''
            INSERT INTO TaiKhoan (email_dang_nhap, mat_khau, quyen)
            VALUES (?, ?, ?)
        ''', (self.email_dang_nhap, hashed_password, self.quyen))

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()
        return True  # Trả về True khi tạo tài khoản thành công
    @staticmethod
    def lay_ma_tai_khoan(email_dang_nhap):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT ma_tai_khoan FROM TaiKhoan WHERE email_dang_nhap = ?
        ''', (email_dang_nhap,))
        ma_tai_khoan = cursor.fetchone()

        conn.close()
        return ma_tai_khoan[0] if ma_tai_khoan else None
    
    def kiem_tra_dang_nhap(email, password):
        # Kết nối cơ sở dữ liệu
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Mã hóa mật khẩu giống như khi đăng ký
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Truy vấn kiểm tra email và mật khẩu
        cursor.execute('''SELECT * FROM TaiKhoan WHERE email_dang_nhap = ? AND mat_khau = ?''', (email, hashed_password))
        tai_khoan = cursor.fetchone()

        conn.close()

        # Nếu có tài khoản, trả về thông tin tài khoản, ngược lại trả về None
        if tai_khoan:
            return tai_khoan
        else:
            return False
        
    def cap_nhat_email(ma_tai_khoan, email):
        try:
            # Kết nối đến cơ sở dữ liệu SQLite
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            print("Cập nhật email cho tài khoản với mã:", ma_tai_khoan)

            # Cập nhật email vào bảng TaiKhoan
            cursor.execute('''
                UPDATE TaiKhoan
                SET email_dang_nhap = ?
                WHERE ma_tai_khoan = ?
            ''', (email, ma_tai_khoan))

            # Kiểm tra xem có dòng nào bị ảnh hưởng không
            if cursor.rowcount > 0:
                print("Cập nhật email thành công!")
            else:
                print("Không tìm thấy tài khoản với mã này!")

            # Lưu thay đổi và đóng kết nối
            connection.commit()

        except sqlite3.Error as e:
            print("Lỗi khi cập nhật email:", e)
        finally:
            connection.close()

    @staticmethod
    def xoa_tai_khoan_theo_ma_tai_khoan(ma_tai_khoan):
        """Xóa tài khoản theo mã tài khoản."""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Xóa tài khoản dựa trên mã tài khoản
        cursor.execute('DELETE FROM TaiKhoan WHERE ma_tai_khoan = ?', (ma_tai_khoan,))
        print("abc xóa rồi nè")
        
        # Kiểm tra xem có dòng nào bị ảnh hưởng không
        if cursor.rowcount > 0:
            print("Xóa tài khoản thành công!")
        else:
            print("Không tìm thấy tài khoản với mã tài khoản này!")

        connection.commit()
        connection.close()

    @staticmethod
    def lay_danh_sach_email():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Truy vấn lấy tất cả các email trong bảng TaiKhoan
        cursor.execute("SELECT email_dang_nhap FROM TaiKhoan")
        
        # Lấy tất cả các kết quả và lưu vào một danh sách
        emails = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return emails

    @staticmethod
    def getRole(email):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT quyen FROM TaiKhoan where email_dang_nhap = ?", (email,))
        roles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return roles
