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
azure_endpoint = "서비스키"
azure_key = "엔드포인트"

@app.route('/')
def index():
    # 루트 경로에 접근하면 /files 경로로 리다이렉션합니다.
    return redirect(url_for('files'))

@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            timestamp = datetime.now().strftime('%y%m%d%H%M')
            filename = secure_filename(file.filename)
            new_filename = f"{timestamp}_{filename}"
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)

            # Azure Document Intelligence로부터 텍스트 추출
            text_results = analyze_document(azure_endpoint, azure_key, file_path)

            # 추출된 모든 텍스트를 콘솔에 출력
            print("추출된 텍스트:")
            for text in text_results:
                print(text)

            data = extract_data(text_results)
            csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"data_{new_filename}.csv")
            append_data_to_csv(data, csv_file_path)

            return render_template('result.html', csv_filename=f"data_{new_filename}.csv")
    else:
        return render_template('files.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=9999, debug=True)
