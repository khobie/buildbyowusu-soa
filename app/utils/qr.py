import os
import qrcode
from flask import current_app, url_for


def generate_student_qr(student):
    data = f'RIDGE|{student.student_id}|{student.user.full_name}'
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#1E40AF', back_color='white')
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles')
    os.makedirs(folder, exist_ok=True)
    filename = f'qr_{student.student_id}.png'
    path = os.path.join(folder, filename)
    img.save(path)
    return f'uploads/profiles/{filename}'
