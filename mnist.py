import os
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from deepface import DeepFace

app = Flask(__name__)

# 保存先設定
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ランキングデータ保持用
ranking_history = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_smile(img_path):
    try:
        results = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
        smile_score = results[0]['emotion']['happy']
        return round(float(smile_score), 1)
    except Exception as e:
        print(f"解析エラー: {e}")
        return 0.0

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        
        if not files or files[0].filename == '':
            return render_template("index.html", answer="画像が選択されていません", ranking=ranking_history)

        last_image_url = None
        count_high_score = 0

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                score = analyze_smile(filepath)
                if score >= 85:
                    count_high_score += 1
                
                new_entry = {
                    'filename': filename, # ファイル名を保持
                    'score': score,
                    'url': url_for('static', filename='uploads/' + filename)
                }
                ranking_history.append(new_entry)
                last_image_url = new_entry['url']

        ranking_history.sort(key=lambda x: x['score'], reverse=True)
        
        msg = f"解析完了：{len(files)}枚中、{count_high_score}枚が85点以上でした！"
        return render_template("index.html", answer=msg, image_url=last_image_url, ranking=ranking_history[:10])

    return render_template("index.html", answer=None, image_url=None, ranking=ranking_history)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)