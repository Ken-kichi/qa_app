from . import db
from datetime import datetime
import uuid
from dateutil import tz


class PDFFile(db.Model):
    # PDFファイルを表すデータベースモデル
    id = db.Column(
        db.String(36),  # 一意の識別子
        primary_key=True,
        default=lambda: str(uuid.uuid4())  # UUIDをデフォルト値として使用
    )
    filename = db.Column(db.String(128), nullable=False)  # ファイル名
    upload_time = db.Column(
        db.DateTime, default=lambda: datetime.now(tz.gettz("Asia/Tokyo")))  # アップロード時間
    filepath = db.Column(db.String(256), nullable=False)  # ファイルパス

    def __repr__(self):
        # PDFFileオブジェクトの文字列表現
        return f'<PDFFile {self.filename}>'
