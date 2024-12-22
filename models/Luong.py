import sqlite3
from datetime import datetime
class Luong:
    def __init__(self, ma_luong, ma_nhan_vien, thang, nam, so_ngay_di_lam, so_ngay_di_muon, tong_luong):
        self.ma_luong = ma_luong
        self.ma_nhan_vien = ma_nhan_vien
        self.thang = thang
        self.nam = nam
        self.so_ngay_di_lam = so_ngay_di_lam
        self.so_ngay_di_muon = so_ngay_di_muon
        self.tong_luong = tong_luong


    @staticmethod
    def add_luong(ma_nhan_vien, thang, nam, so_ngay_di_lam, so_ngay_di_muon, tong_luong):
        """
        Thêm thông tin lương cho nhân viên
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Luong (ma_nhan_vien, thang, nam, so_ngay_di_lam, so_ngay_di_muon, tong_luong)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (ma_nhan_vien, thang, nam, so_ngay_di_lam, so_ngay_di_muon, tong_luong))
        conn.commit()
        conn.close()

    @staticmethod
    def update_luong(ma_luong, so_ngay_di_lam, so_ngay_di_muon, tong_luong):
        """
        Cập nhật thông tin lương cho nhân viên
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Luong
            SET so_ngay_di_lam = ?, so_ngay_di_muon = ?, tong_luong = ?
            WHERE ma_luong = ?
        ''', (so_ngay_di_lam, so_ngay_di_muon, tong_luong, ma_luong))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_luong(ma_luong):
        """
        Xóa thông tin lương của nhân viên
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Luong WHERE ma_luong = ?', (ma_luong,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_luong():
        """
        Lấy tất cả thông tin lương của tất cả nhân viên
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Luong')
        rows = cursor.fetchall()
        conn.close()
        return [Luong(*row) for row in rows]

    @staticmethod
    def lay_danh_sach_nhan_vien_va_luong(thang=None, nam=None, search=None):
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            
            query = '''
                SELECT
                    luong.thang,
                    luong.nam,
                    luong.ma_luong, 
                    luong.ma_nhan_vien, 
                    nhanvien.ho_ten,
                    nhanvien.so_dien_thoai, 
                    nhanvien.email,
                    luong.so_ngay_di_lam, 
                    luong.so_ngay_di_muon, 
                    luong.tong_luong
                FROM Luong
                JOIN NhanVien ON Luong.ma_nhan_vien = NhanVien.ma_nhan_vien
            '''

            filters = []
            if thang:
                filters.append(f'luong.thang = {thang}')
            if nam:
                filters.append(f'luong.nam = {nam}')
            if search:
                filters.append(f'nhanvien.ho_ten LIKE "%{search}%"')

            if filters:
                query += ' WHERE ' + ' AND '.join(filters)

            cursor.execute(query)
            records = cursor.fetchall()
            connection.close()

            # Tạo danh sách các đối tượng từ dữ liệu trả về
            danh_sach = []
            for record in records:
                danh_sach.append({
                    'thang': record[0],
                    'nam': record[1],
                    'ma_luong': record[2],
                    'ma_nhan_vien': record[3],
                    'ho_ten': record[4],
                    'so_dien_thoai': record[5],
                    'email': record[6],
                    'so_ngay_di_lam': record[7],
                    'so_ngay_di_muon': record[8],
                    'tong_luong': record[9],
                })

            return danh_sach

        except sqlite3.Error as e:
            print(f"Lỗi khi lấy danh sách nhân viên: {e}")
            return []
        
    def get_luong_by_nhanvien_id(ma_nhan_vien):
        """
        Lấy danh sách thông tin lương của nhân viên theo mã nhân viên và trả về dưới dạng danh sách.
        """
        try:
            # Kết nối đến cơ sở dữ liệu
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Truy vấn thông tin lương theo mã nhân viên
            cursor.execute('''
                SELECT ma_luong, thang, nam, so_ngay_di_lam, so_ngay_di_muon, tong_luong
                FROM Luong
                WHERE ma_nhan_vien = ?
            ''', (ma_nhan_vien,))

            # Lấy tất cả kết quả
            rows = cursor.fetchall()
            conn.close()

            # Chuyển đổi kết quả thành danh sách từ điển
            salary_list = [
                {
                    "ma_luong": row[0],
                    "thang": row[1],
                    "nam": row[2],
                    "so_ngay_di_lam": row[3],
                    "so_ngay_di_muon": row[4],
                    "tong_luong": row[5],
                }
                for row in rows
            ]

            return salary_list

        except sqlite3.Error as e:
            print(f"Lỗi khi lấy thông tin lương: {e}")
            return []
        



    def tong_hop_luong_cuoi_thang(ma_nhan_vien):
        # Lấy tháng và năm hiện tại
        now = datetime.now()
        thang_hien_tai = now.strftime('%m')  # Tháng hiện tại
        nam_hien_tai = now.strftime('%Y')  # Năm hiện tại

        # Lấy tháng và năm trước đó (tháng 11 khi hiện tại là tháng 12)
        if int(thang_hien_tai) == 1:
            thang_truoc = 12
            nam_truoc = str(int(nam_hien_tai) - 1)
        else:
            thang_truoc = int(thang_hien_tai) - 1
            nam_truoc = nam_hien_tai

        # Chuyển thang_truoc thành dạng 2 chữ số (ví dụ: 01, 02, ... 12)
        thang_truoc = f"{thang_truoc:02}"

        # Kiểm tra xem lương đã được tổng hợp cho tháng trước chưa
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Kiểm tra xem đã có dữ liệu lương cho tháng trước chưa
        cursor.execute('''SELECT COUNT(*) FROM Luong WHERE thang = ? AND nam = ? AND ma_nhan_vien = ?''', (thang_truoc, nam_truoc, ma_nhan_vien))
        result = cursor.fetchone()

        if result[0] > 0:
            print(f"Lương đã được tổng hợp cho tháng {thang_truoc} {nam_truoc} cho nhân viên {ma_nhan_vien}.")
        else:
            print(f"Tổng hợp lương cho tháng {thang_truoc} {nam_truoc} cho nhân viên {ma_nhan_vien}...")

            try:
                # Debug: Kiểm tra dữ liệu trong bảng ChamCong
                cursor.execute('''
                    SELECT strftime('%m', ngay), strftime('%Y', ngay), trang_thai
                    FROM ChamCong
                    WHERE ma_nhan_vien = ?
                    ''', (ma_nhan_vien,))
                cham_cong_data = cursor.fetchall()
                if cham_cong_data:
                    print(f"Dữ liệu chấm công cho nhân viên {ma_nhan_vien}: {cham_cong_data}")
                else:
                    print(f"Không có dữ liệu chấm công cho nhân viên {ma_nhan_vien}.")
                
                # Thực hiện tổng hợp lương cho tháng trước (ví dụ tháng 11) cho nhân viên cụ thể
                cursor.execute('''
                    INSERT INTO Luong (ma_nhan_vien, thang, nam, so_ngay_di_lam, so_ngay_di_muon, tong_luong)
                    SELECT ma_nhan_vien, ?, ?, 
                        SUM(CASE WHEN trang_thai = 'Đi làm' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN trang_thai = 'Đi muộn' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN trang_thai = 'Đi làm' THEN 100 ELSE 0 END) + 
                        SUM(CASE WHEN trang_thai = 'Đi muộn' THEN 50 ELSE 0 END) AS tong_luong
                    FROM ChamCong
                    WHERE ma_nhan_vien = ? AND strftime('%m', ngay) = ? AND strftime('%Y', ngay) = ?
                    GROUP BY ma_nhan_vien
                ''', (thang_truoc, nam_truoc, ma_nhan_vien, thang_truoc, nam_truoc))

                connection.commit()  # Lưu thay đổi vào cơ sở dữ liệu
                print(f"Tổng hợp lương cho tháng {thang_truoc} {nam_truoc} thành công cho nhân viên {ma_nhan_vien}.")

            except sqlite3.Error as e:
                print("Lỗi khi chèn dữ liệu vào bảng Luong:", e)

        connection.close()

    @staticmethod
    def xoa_luong_theo_ma_nhan_vien(ma_nhan_vien):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Luong WHERE ma_nhan_vien = ?', (ma_nhan_vien,))
        connection.commit()
        connection.close()

