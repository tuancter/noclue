import sqlite3
from datetime import datetime

class ChamCong:
    def __init__(self, ma_cham_cong=None, ma_nhan_vien=None, ngay=None, gio_vao=None, gio_ra=None, trang_thai=None, phuong_thuc=None):
        self.ma_cham_cong = ma_cham_cong
        self.ma_nhan_vien = ma_nhan_vien
        self.ngay = ngay
        self.gio_vao = gio_vao
        self.gio_ra = gio_ra
        self.trang_thai = trang_thai
        self.phuong_thuc = phuong_thuc

    @staticmethod
    def create_table():
        """Tạo bảng ChamCong trong cơ sở dữ liệu."""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChamCong (
                ma_cham_cong INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_nhan_vien INTEGER NOT NULL,
                ngay DATE NOT NULL,
                gio_vao TIME,
                gio_ra TIME,
                trang_thai TEXT CHECK(trang_thai IN ('Đi làm', 'Đi muộn', 'Không đi làm')) NOT NULL,
                FOREIGN KEY (ma_nhan_vien) REFERENCES NhanVien(ma_nhan_vien)
                phuong_thuc TEXT CHECK(phuong_thuc IN ('Nhận diện', 'Thủ công')) NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    @staticmethod
    def getID(ma_nhan_vien):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT ma_cham_cong FROM ChamCong where ma_nhan_vien = ? ORDER BY ma_cham_cong DESC LIMIT 1', (ma_nhan_vien,))
        record = cursor.fetchone()
        connection.close()
        if record is None:
            return False
        else:
            return record[0]

    @staticmethod
    def them_cham_cong(ma_nhan_vien, ngay, gio_vao, gio_ra, phuong_thuc, trang_thai):
        """Thêm một bản ghi chấm công mới."""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO ChamCong (ma_nhan_vien, ngay, gio_vao, gio_ra, phuong_thuc,trang_thai)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (ma_nhan_vien, ngay, gio_vao, gio_ra, phuong_thuc, trang_thai))
        connection.commit()
        connection.close()

    @staticmethod
    def lay_danh_sach_cham_cong(ma_nhan_vien):
        """Lấy danh sách chấm công của một nhân viên cụ thể."""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT ma_cham_cong, ngay, gio_vao, gio_ra, trang_thai
            FROM ChamCong
            WHERE ma_nhan_vien = ?
        ''', (ma_nhan_vien,))
        records = cursor.fetchall()
        connection.close()
        return records


    @staticmethod
    def cap_nhat_cham_cong(ma_cham_cong, status, start_time, end_time):
        # Kết nối đến cơ sở dữ liệu SQLite
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        print("status là: ", status)
        # Cập nhật dữ liệu vào bảng ChamCong
        cursor.execute('''
            UPDATE ChamCong
            SET trang_thai = ?, gio_vao = ?, gio_ra = ?
            WHERE ma_cham_cong = ?
        ''', (status, start_time, end_time, ma_cham_cong))
        print("thành công!!!!!")
        # Lưu thay đổi và đóng kết nối
        connection.commit()
        connection.close()

    @staticmethod
    def xoa_cham_cong(ma_cham_cong):
        """Xóa một bản ghi chấm công."""
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM ChamCong WHERE ma_cham_cong = ?', (ma_cham_cong,))
        connection.commit()
        connection.close()

    def lay_thong_tin_cham_cong_theo_id(ma_cham_cong):
        # Kết nối đến cơ sở dữ liệu SQLite
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Truy vấn để lấy thông tin chấm công theo ma_cham_cong
        cursor.execute('''
            SELECT *
            FROM ChamCong
            WHERE ma_cham_cong = ?
        ''', (ma_cham_cong,))

        # Lấy kết quả từ câu truy vấn
        record = cursor.fetchone()
        
        # Đóng kết nối
        connection.close()

        if record:
            # Trả về một đối tượng NhanVien với thông tin từ cơ sở dữ liệu
            chamcong = ChamCong(
                ma_cham_cong=record[0],
                ma_nhan_vien=record[1],
                ngay=record[2],
                gio_vao=record[3],
                gio_ra=record[4],
                trang_thai=record[5],
                phuong_thuc=record[6]
            )
            return chamcong
        else:
            return None
        
    @staticmethod
    def end_time(ma_cham_cong, end_time):
        # Kết nối đến cơ sở dữ liệu SQLite
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # Cập nhật dữ liệu vào bảng ChamCong
        cursor.execute('''
            UPDATE ChamCong
            SET gio_ra = ?
            WHERE ma_cham_cong = ?
        ''', (end_time, ma_cham_cong))
        print("thành công!!!!!")
        # Lưu thay đổi và đóng kết nối
        connection.commit()
        connection.close()

    @staticmethod
    def getManuals():
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM ChamCong WHERE phuong_thuc = "Thủ công"')
        records = cursor.fetchall()
        connection.close()
        return records
    
    def getTimetracksByEmployeeID(ma_nhan_vien):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM ChamCong WHERE ma_nhan_vien = ?', (ma_nhan_vien,))
        records = cursor.fetchall()
        connection.close()
        return records

