from db import db
 
class File(db.Model):
    """
    File MODEL

    """

    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    error_id = db.Column(db.Integer, db.ForeignKey('errors.id'))
    version = db.Column(db.String, nullable=False)
    presigned_url = db.Column(db.String)
    
    def __repr__(self):
        return f"<File: ID: {self.id}, Name: {self.file_name}, Error ID: {self.error_id}, Version: {self.version}"
