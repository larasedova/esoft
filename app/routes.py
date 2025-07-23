from flask import Blueprint, request, jsonify, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename
from models.db_models import File, AnalysisResult
from app import db
from utils.data_processing import analyze_data, clean_data
import matplotlib.pyplot as plt

bp = Blueprint('api', __name__)

# Конфигурация загрузки файлов
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 415

    try:
        # Сохранение файла
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Сохранение в базу данных
        new_file = File(filename=filename, filepath=filepath)
        db.session.add(new_file)
        db.session.commit()

        # Анализ данных
        analysis_result = analyze_data(filepath)

        # Сохранение результатов анализа
        new_analysis = AnalysisResult(
            file_id=new_file.id,
            mean_values=analysis_result['mean'],
            median_values=analysis_result['median'],
            correlation_matrix=analysis_result['correlation']
        )
        db.session.add(new_analysis)
        db.session.commit()

        return jsonify({
            'message': 'File uploaded and analyzed successfully',
            'file_id': new_file.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400