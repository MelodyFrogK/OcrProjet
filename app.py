from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from document_analysis import analyze_document
from csv_writer import extract_data, append_data_to_csv
import re
from flask import send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Azure 서비스 키와 엔드포인트 설정
azure_endpoint = "https://t-ocr.cognitiveservices.azure.com/"
azure_key = "e4b9d545f7ef4461a7ceedb920f46ef2"

@app.route('/')
def index():
    # 루트 경로에 접근하면 /files 경로로 리다이렉션합니다.
    return redirect(url_for('files'))

@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        files = request.files.getlist('file') # 복수 파일 처리
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Azure Document Intelligence로부터 텍스트 추출
                text_results = analyze_document(azure_endpoint, azure_key, file_path)

                # 추출된 데이터를 처리하여 CSV 파일에 추가
                data = extract_data(text_results)
                # CSV 파일명을 고정합니다.
                csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "fixed_data.csv")
                append_data_to_csv(data, csv_file_path)

        return render_template('result.html', csv_filename="fixed_data.csv")
    else:
        return render_template('files.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=9999, debug=True)
