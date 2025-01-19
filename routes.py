import os
from flask import render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from . import db
from .models import PDFFile
from . import create_app

app = create_app()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def index():
    return "<p>Hello World!</p>"


@app.route('/uploaded_list')
def uploaded_list():
    files = PDFFile.query.all()
    return render_template('list.html', files=files)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            pdf = PDFFile(filename=filename, filepath=filepath)
            db.session.add(pdf)
            db.session.commit()
            flash('File uploaded successfully!')
            return redirect(url_for('index'))
        flash('Invalid file type!')
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
