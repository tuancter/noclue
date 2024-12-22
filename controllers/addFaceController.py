from flask import render_template, Blueprint, request, jsonify, session, redirect, url_for
import os
import base64

face = Blueprint("face", __name__, static_folder='static', template_folder='templates')

@face.route("/", methods=["GET", "POST"])
def add_face():
    if 'ma_tai_khoan' not in session:
        return redirect(url_for('dangnhapnhanvien.dangnhap_nhanvien'))
    return render_template('face_register.html')

@face.route("/upload", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not os.path.exists('uploads/face_registers'):
        os.makedirs('uploads/face_registers')
    file.save(os.path.join('uploads/face_registers', 'register_face.png'))
    return jsonify({"success": "Image saved successfully"})

