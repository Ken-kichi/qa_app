from . import db
from datetime import datetime, UTC


class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    upload_time = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    filepath = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<PDFFile {self.filename}>'
