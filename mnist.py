import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import numpy as np
from deepface import DeepFace  # 笑顔判定用

app = Flask(__name__)
app.secret_key = "aidemy"

# --- 設定 ---
UPLOAD_FOLDER = "/tmp/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 笑顔判定ロジック
def analyze_smile(filepath):
    try:
        results = DeepFace.analyze(
            img_path=filepath, 
            actions=['emotion'],
            enforce_detection=True
        )
        # 全員の笑顔スコアの平均などを計算（今回は1人目を基準）
        score = results[0]['emotion']['happy']
        if score > 80:
            return f"笑顔スコア: {score:.1f}点！最高だッ！年賀状確定だッ！"
        else:
            return f"笑顔スコア: {score:.1f}点。もう少し笑顔が欲しいところだぜ…"
    except Exception as e:
        return f"顔が見つかりませんでしたッ！（{str(e)}）"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 笑顔判定を実行
        pred_answer = analyze_smile(filepath)

        # 処理後に一時ファイルを削除
        if os.path.exists(filepath):
            os.remove(filepath)

        return render_template("index.html", answer=pred_answer)

    return render_template("index.html", answer="")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)