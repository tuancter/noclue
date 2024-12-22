// Hiển thị modal chỉnh sửa
function openEditModal() {
    document.getElementById('editModal').style.display = 'flex';
}

// Đóng modal chỉnh sửa
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Lưu thay đổi
function saveChanges() {
    alert('Đã lưu thay đổi!');
    closeModal();
}


document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function () {
            const ma_nhan_vien = this.getAttribute('data-id');
            console.log('Mã nhân viên:', ma_nhan_vien);  // Kiểm tra giá trị maChamCong
            
            if (!ma_nhan_vien) {
                console.error('Không có mã nhân viên hợp lệ.');
                alert('Không tìm thấy mã nhân viên.');
                return;
            }

            fetch(`/admin_trangchu/lay_thong_tin_nhan_vien/${ma_nhan_vien}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Dữ liệu không tồn tại');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);  // Kiểm tra dữ liệu trả về
                    document.getElementById('name').value = data.ho_ten || '';
                    document.getElementById('dob').value = data.ngay_sinh || '';
                    document.getElementById('position').value = data.vi_tri || '';
                    document.getElementById('phone').value = data.so_dien_thoai || '';
                    document.getElementById('email').value = data.email || '';
                    document.getElementById('address').value = data.dia_chi || '';

                    // Mở modal sau khi dữ liệu đã được tải
                    openEditModal();
                    document.getElementById('editModal').setAttribute('data-id', ma_nhan_vien);
                })
                .catch(error => {
                    console.error('Lỗi:', error);
                    alert('Không thể tải dữ liệu nhân viên font end.');
                });
        });
    });
});



// Lưu thay đổi
function saveChanges() {
    const ma_nhan_vien = document.getElementById('editModal').getAttribute('data-id');
    const ho_ten = document.getElementById('name').value;
    const dia_chi = document.getElementById('address').value;
    const ngay_sinh = document.getElementById('dob').value;
    const vi_tri = document.getElementById('position').value;
    const email = document.getElementById('email').value;
    const so_dien_thoai = document.getElementById('phone').value;

    // Dữ liệu để gửi lên backend
    const updatedData = {
        ma_nhan_vien: ma_nhan_vien,
        ho_ten: ho_ten,
        dia_chi: dia_chi,
        ngay_sinh: ngay_sinh,
        vi_tri: vi_tri,
        email: email,
        so_dien_thoai: so_dien_thoai
    };

    // Gửi yêu cầu cập nhật dữ liệu
    fetch(`/admin_trangchu/cap_nhat_nhan_vien/${ma_nhan_vien}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Cập nhật thành công');
        // Cập nhật giao diện (cập nhật thông tin trong bảng)
        const row = document.querySelector(`[data-id="${ma_nhan_vien}"]`).closest('tr');
        row.querySelector('.name').innerText = ho_ten;
        row.querySelector('.dob').innerText = ngay_sinh;
        row.querySelector('.email').innerText = email;
        row.querySelector('.address').innerText = dia_chi;
        row.querySelector('.position').innerText = vi_tri;

        // Đóng modal sau khi lưu
        closeModal();
    })
    .catch(error => {
        alert('Không thể cập nhật thông tin nhân viên.');
    });
}

function xacNhanXoa(button) {
    var maNhanVien = button.getAttribute("data-id");
    console.log("Mã nhân viên cần xóa: " + maNhanVien);  // Kiểm tra giá trị nhận được

    if (confirm("Bạn có chắc chắn muốn xóa nhân viên này không?")) {
        fetch(`/admin_trangchu/xoa_nhan_vien/${maNhanVien}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);  // Hiển thị thông báo thành công
            location.reload();  // Reload trang sau khi xóa
        })
        .catch(error => console.error("Lỗi khi xóa:", error));
    }
}

