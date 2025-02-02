import os
from flask import render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from . import db
from .models import PDFFile
from . import create_app
from .Langchain_utils import Langchain_utils
from dotenv import load_dotenv
from markupsafe import Markup
import markdown

# 環境変数の読み込み
load_dotenv()
app = create_app()

# アップロードを許可するファイルタイプを確認する関数


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ホームページのルート


@app.route("/")
def index():
    # データベースから全てのPDFファイルを取得
    files = PDFFile.query.all()
    return render_template('index.html', files=files)

# 質問を処理するルート


@app.route("/ask", methods=["POST"])
def ask_question():
    # フォームから質問とファイルパスを取得
    question = request.form.get("question")
    file_path = request.form.get("file_path")

    # Langchainの初期設定
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

    # 質問に対する回答を取得
    answer = langchain_utils.get_answer(
        model_name="gpt-4o-mini",
        retriever=retriever,
        query=question
    )
    # HTML形式に変換
    answer_html = Markup(markdown.markdown(answer))

    # 再度全てのPDFファイルを取得
    files = PDFFile.query.all()

    return render_template('asked_question.html', answer=answer_html, files=files)

# アップロードされたファイルのリストを表示するルート


@app.route('/uploaded_list')
def uploaded_list():
    # データベースから全てのPDFファイルを取得
    files = PDFFile.query.all()
    return render_template('list.html', files=files)

# ファイルをアップロードするルート


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # アップロードされたファイルを取得
        file = request.files['file']
        # ファイルが有効な場合
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # ファイルを保存
            file.save(filepath)
            # データベースにファイル情報を追加
            pdf = PDFFile(filename=filename, filepath=filepath)
            db.session.add(pdf)
            db.session.commit()
            flash('File uploaded successfully!')
            return redirect(url_for('uploaded_list'))
        flash('Invalid file type!')
    return render_template('upload.html')

# アップロードされたファイルを提供するルート


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ファイルを削除するルート


@app.route('/delete', methods=['POST'])
def delete():
    # フォームからファイルIDを取得
    fileId = request.form.get("fileId")
    file = PDFFile.query.filter_by(id=fileId).first()

    if file:
        # データベースからファイルを削除
        db.session.delete(file)
        db.session.commit()
        # サーバーからファイルを削除
        os.remove(file.filepath)
        flash('File deleted successfully!')
    else:
        flash('File not found!')

    return redirect(url_for('uploaded_list'))
