// document.getElementById('registrationForm').addEventListener('submit', function (e) {
//     e.preventDefault();

//     const fullName = document.getElementById('fullName').value.trim();
//     const birthDate = document.getElementById('birthDate').value;
//     const address = document.getElementById('address').value.trim();
//     const phoneNumber = document.getElementById('phoneNumber').value.trim();
//     const email = document.getElementById('email').value.trim();
//     const position = document.getElementById('position').value.trim();
//     const password = document.getElementById('password').value;
//     const confirmPassword = document.getElementById('confirmPassword').value;

//     // Kiểm tra các trường nhập liệu
//     const data = {
//         fullName: fullName,
//         birthDate: birthDate,
//         address: address,
//         phoneNumber: phoneNumber,
//         email: email,
//         position: position,
//         password: password,
//         confirmPassword: confirmPassword
//     };

//     // Gửi dữ liệu dưới dạng JSON
//     fetch("{{ url_for('dangky.add_nhanvien') }}", {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)  // Dữ liệu gửi đi
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.message) {
//             alert(data.message);
//         } else {
//             alert('Đăng ký không thành công!');
//         }
//     })
//     .catch(error => {
//         alert('Có lỗi xảy ra: ' + error);
//     });
// });

// fetch("{{ url_for('dangky.add_nhanvien') }}", {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(data)
// })
// .then(response => {
//     // In ra nội dung phản hồi từ server để kiểm tra
//     return response.text();  // Chúng ta sẽ kiểm tra dạng text thay vì JSON ở đây
// })
// .then(text => {
//     console.log("Server Response:", text);  // In ra phản hồi dưới dạng văn bản
//     try {
//         const data = JSON.parse(text);  // Chúng ta thử phân tích bằng JSON.parse
//         if (data.message) {
//             alert(data.message);
//         } else {
//             alert('Đăng ký không thành công!');
//         }
//     } catch (error) {
//         alert('Có lỗi xảy ra khi phân tích JSON: ' + error);
//     }
// })
// .catch(error => {
//     alert('Có lỗi xảy ra: ' + error);
// });
