// Xử lý mở modal quên mật khẩu
document.getElementById("forgot-password-link").addEventListener("click", function(event) {
    event.preventDefault();  // Ngừng hành động mặc định của link
    document.getElementById("forgot-password-modal").style.display = "flex";
});

// Xử lý đóng modal quên mật khẩu
document.getElementById("close-modal").addEventListener("click", function() {
    document.getElementById("forgot-password-modal").style.display = "none";
});

// Xử lý khi người dùng gửi form quên mật khẩu
document.getElementById("forgot-password-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const resetEmail = document.getElementById("reset-email").value;

    // Kiểm tra email hợp lệ
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(resetEmail)) {
        alert("Vui lòng nhập email hợp lệ.");
        return;
    }

    // Gửi yêu cầu khôi phục mật khẩu (thực tế bạn cần xử lý với server ở đây)
    alert("Một email khôi phục mật khẩu đã được gửi đến " + resetEmail);
    document.getElementById("forgot-password-modal").style.display = "none";
});
