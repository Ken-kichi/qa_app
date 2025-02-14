import os


class Config:
    # データベースのURIを環境変数から取得
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:GDOUzrnVRdL4jivgQrLy7chD9t9AfVmW@dpg-cumug7aj1k6c73b442gg-a.singapore-postgres.render.com/pdf_db_957f")
    # SQLAlchemyの変更追跡を無効にする
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # アップロードフォルダのパスを設定
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # 許可されるファイル拡張子のセット
    ALLOWED_EXTENSIONS = {'pdf'}  # PDFファイルのみ許可
