from datetime import datetime
from app import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    analyses = db.relationship('AnalysisResult', backref='file', lazy=True)

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    mean_values = db.Column(db.JSON)  # Хранение средних значений
    median_values = db.Column(db.JSON)  # Хранение медиан
    correlation_matrix = db.Column(db.JSON)  # Матрица корреляции
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)