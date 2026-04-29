import os
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from deepface import DeepFace
from PIL import Image, ImageOps
import pillow_heif

# HEIC対応
pillow_heif.register_heif_opener()

app = Flask(__name__)

# 保存先設定
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'HEIC'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ランキング履歴を保持
ranking_history = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_smile(img_path):
    try:
        # 1. 画像を開き、向きを補正
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)

        # 2. リサイズ
        max_size = 1200
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # 3. ファイル名生成（GUIアプリとの連携用）
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        new_filename = base_name + ".jpg"
        new_jpg_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        # 4. JPGとして保存
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(new_jpg_path, "JPEG", quality=90)

        # 5. AI解析
        results = DeepFace.analyze(
            img_path=new_jpg_path, 
            actions=['emotion'], 
            enforce_detection=False,
            detector_backend='retinaface'
        )
        
        scores = []
        for face in results:
            scores.append(round(float(face['emotion']['happy']), 1))
        
        scores.sort(reverse=True)
        score_details = ", ".join(map(str, scores))
        
        top_score = scores[0] if scores else 0.0
        face_count = len(scores)
        
        return top_score, face_count, score_details, new_filename

    except Exception as e:
        print(f"解析エラー: {e}")
        return 0.0, 0, "N/A", os.path.basename(img_path)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if not files or files[0].filename == '':
            return render_template("index.html", answer="画像が選択されていません", ranking=ranking_history)

        count_high_score = 0
        last_image_url = None

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                score, face_count, details, final_filename = analyze_smile(filepath)
                if score >= 85:
                    count_high_score += 1
                
                new_entry = {
                    'filename': final_filename,
                    'score': score,
                    'face_count': face_count,
                    'details': details,
                    'url': url_for('static', filename='uploads/' + final_filename)
                }
                ranking_history.append(new_entry)
                last_image_url = new_entry['url']

        ranking_history.sort(key=lambda x: x['score'], reverse=True)
        msg = f"解析完了：{len(files)}枚中、{count_high_score}枚が85点以上でした！"
        return render_template("index.html", answer=msg, image_url=last_image_url, ranking=ranking_history)

    return render_template("index.html", answer=None, image_url=None, ranking=ranking_history)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)