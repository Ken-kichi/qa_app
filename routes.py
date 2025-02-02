import os
from flask import render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from . import db
from .models import PDFFile
from . import create_app
from .Langchain_utils import Langchain_utils
import os
from dotenv import load_dotenv
from markupsafe import Markup
import markdown

load_dotenv()
app = create_app()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def index():
    files = PDFFile.query.all()
    return render_template('index.html', files=files)


@app.route("/ask", methods=["POST"])
def ask_question():
    question = request.form.get("question")
    file_path = request.form.get("file_path")

    # 初期設定
    langchain_utils = Langchain_utils(
        api_key=os.getenv("OPENAI_KEY"),
        chunk_size=100,
        chunk_overlap=10,
        model="text-embedding-3-small",
        query=question
    )

    # PDFから情報を検索
    document = langchain_utils.get_pdf_contents(file_path)
    contents = langchain_utils.get_contents(document)
    retriever = langchain_utils.get_retriever(contents)

    answer = langchain_utils.get_answer(
        model_name="gpt-4o-mini",
        retriever=retriever,
        query=question
    )
    answer_html = Markup(markdown.markdown(answer))

    files = PDFFile.query.all()

    return render_template('asked_question.html', answer=answer_html, files=files)


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
            return redirect(url_for('uploaded_list'))
        flash('Invalid file type!')
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
