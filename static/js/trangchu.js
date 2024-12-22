// Đây là nơi bạn có thể xử lý các sự kiện JavaScript nếu cần, chẳng hạn như xác thực form, chuyển hướng, v.v.
document.querySelector(".btn-login").addEventListener("click", function(e) {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Kiểm tra nếu thông tin không hợp lệ
    if (!email || !password) {
        e.preventDefault();
        alert("Vui lòng điền đầy đủ thông tin!");
    }
});
