let currentRowId = null;

// Chức năng tìm kiếm theo ngày
function searchAttendance() {
    var inputDate = document.getElementById('searchDate').value;
    var table = document.getElementById('attendanceData');
    var rows = table.getElementsByTagName('tr');
    
    // Lọc các dòng trong bảng theo ngày
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        if (cells.length > 0) {
            var dateCell = cells[0].textContent || cells[0].innerText;
            if (dateCell.includes(inputDate)) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}

//day du lieu tu server len modal
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function () {
            const maChamCong = this.getAttribute('data-id');
            console.log('Mã chấm công:', maChamCong);  // Kiểm tra giá trị maChamCong
            
            if (!maChamCong) {
                console.error('Không có maChamCong hợp lệ.');
                alert('Không tìm thấy mã chấm công.');
                return;
            }

            fetch(`thongkechamcong/lay_thong_tin_cham_cong/${maChamCong}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Dữ liệu không tồn tại');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);  // Kiểm tra dữ liệu trả về
                    document.getElementById('status').value = data.status || '';
                    document.getElementById('start-time').value = data.start_time || '';
                    document.getElementById('end-time').value = data.end_time || '';
                    document.getElementById('editModal').setAttribute('data-id', maChamCong);
                    document.getElementById('editModal').classList.add('show');
                })
                .catch(error => {
                    console.error('Lỗi:', error);
                    alert('Không thể tải dữ liệu chấm công.');
                });
        });
    });
});

// Đóng modal khi nhấn "Hủy"
function closeModal() {
    document.getElementById('editModal').classList.remove('show');
}

//lưu thay đổi khi bấm nút lưu
function saveChanges() {
    const maChamCong = document.getElementById('editModal').getAttribute('data-id');
    const status = document.getElementById('status').value;
    const start_time = document.getElementById('start-time').value;
    const end_time = document.getElementById('end-time').value;

    const validStatuses = ['Đi làm', 'Đi muộn', 'Không đi làm'];
    if (!validStatuses.includes(status)) {
        alert('Trạng thái không hợp lệ');
        return;
    }
    // Dữ liệu để gửi lên backend
    const updatedData = {
        status: status,
        start_time: start_time,
        end_time: end_time
    };

    // Gửi yêu cầu cập nhật dữ liệu
    fetch(`thongkechamcong/cap_nhat_cham_cong/${maChamCong}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Cập nhật thành công');
        // Cập nhật giao diện hoặc reload lại dữ liệu
        // Cập nhật giao diện
        document.querySelector(`[data-id="${maChamCong}"]`).closest('tr').querySelector('.status').innerText = status;
        document.querySelector(`[data-id="${maChamCong}"]`).closest('tr').querySelector('.start-time').innerText = start_time;
        document.querySelector(`[data-id="${maChamCong}"]`).closest('tr').querySelector('.end-time').innerText = end_time;
    })
    .catch(error => {
        alert('Không thể cập nhật chấm công từ font end.');
    });
}

