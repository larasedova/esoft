from flask import Blueprint, request, jsonify, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils.data_processing import analyze_data, clean_data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from models.db_models import File, AnalysisResult
from app import db

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


@bp.route('/data/stats/<int:file_id>', methods=['GET'])
def get_stats(file_id):
    analysis = AnalysisResult.query.filter_by(file_id=file_id).first()

    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404

    return jsonify({
        'mean': analysis.mean_values,
        'median': analysis.median_values,
        'correlation': analysis.correlation_matrix
    }), 200


@bp.route('/data/clean/<int:file_id>', methods=['GET'])
def clean_file_data(file_id):
    file = File.query.get(file_id)

    if not file:
        return jsonify({'error': 'File not found'}), 404

    try:
        cleaned_df = clean_data(file.filepath)

        # Сохранение очищенного файла
        cleaned_filename = f"cleaned_{file.filename}"
        cleaned_filepath = os.path.join(UPLOAD_FOLDER, cleaned_filename)

        if file.filename.endswith('.csv'):
            cleaned_df.to_csv(cleaned_filepath, index=False)
        else:
            cleaned_df.to_excel(cleaned_filepath, index=False)

        return jsonify({
            'message': 'Data cleaned successfully',
            'cleaned_file': cleaned_filename
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/data/plot/<int:file_id>', methods=['GET'])
def generate_plot(file_id):
    file = File.query.get(file_id)

    if not file:
        return jsonify({'error': 'File not found'}), 404

    try:
        # Чтение файла
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.filepath)
        else:
            df = pd.read_excel(file.filepath)

        # Создание графика
        plt.figure(figsize=(10, 6))
        df.plot()
        plot_path = os.path.join(UPLOAD_FOLDER, f"plot_{file_id}.png")
        plt.savefig(plot_path)
        plt.close()

        return send_file(plot_path, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

