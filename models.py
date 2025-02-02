from . import db
from datetime import datetime
import uuid
from dateutil import tz


class PDFFile(db.Model):
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4())
                   )
    filename = db.Column(db.String(128), nullable=False)
    upload_time = db.Column(
        db.DateTime, default=lambda: datetime.now(tz.gettz("Asia/Tokyo")))
    filepath = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<PDFFile {self.filename}>'
