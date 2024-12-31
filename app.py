from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pororo import Pororo
import os

# Flask 앱 설정
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'  # 이미지 업로드 경로
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Pororo OCR 모델 초기화
ocr = Pororo(task="ocr")

# 업로드된 파일 확장자 확인
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 메인 페이지 (이미지 업로드)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 파일이 업로드되었는지 확인
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        # 파일 유효성 검사 및 저장
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # OCR 결과 처리
            ocr_result = ocr(file_path)

            # 결과 페이지로 리다이렉트
            return render_template('result.html', result=ocr_result, image_url=file_path)

    return render_template('index.html')

# Flask 실행
if __name__ == '__main__':
    # 업로드 디렉토리 생성
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True, host='0.0.0.0', port=5000)
