import os


class Config:
    # データベースのURIを環境変数から取得
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # SQLAlchemyの変更追跡を無効にする
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # アップロードフォルダのパスを設定
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # 許可されるファイル拡張子のセット
    ALLOWED_EXTENSIONS = {'pdf'}  # PDFファイルのみ許可
