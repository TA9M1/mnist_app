import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, request, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename
from deepface import DeepFace

app = Flask(__name__)
app.secret_key = "aidemy_secret"

# --- 保存先の設定 ---
# static/uploads に保存することでブラウザから写真が見れるようになります
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 1. 笑顔判定の関数（呼び出す前に定義しておく必要があります）
def analyze_smile(filepath):
    try:
        results = DeepFace.analyze(
            img_path=filepath, 
            actions=['emotion'],
            enforce_detection=True
        )
        score = results[0]['emotion']['happy']
        if score > 80:
            return f"笑顔スコア: {score:.1f}点！最高だッ！年賀状確定だッ！"
        else:
            return f"笑顔スコア: {score:.1f}点。もう少し笑顔が欲しいところだぜ…"
    except Exception as e:
        return "顔が見つかりませんでしたッ！"

# 2. メインの処理
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

        # ここで上の関数を呼び出す
        pred_answer = analyze_smile(filepath)

        # 画像表示用のURLを生成
        image_url = url_for('static', filename='uploads/' + filename)

        return render_template("index.html", answer=pred_answer, image_url=image_url)

    return render_template("index.html", answer="", image_url=None)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)