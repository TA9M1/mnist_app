# mnist.py の一部を修正
import os
from flask import Flask, request, redirect, render_template, flash, url_for # url_forを追加
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "aidemy"

# 保存先を static/uploads に変更（これでブラウザから見れるようになります）
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        # 今回は画像を表示させたいので、os.remove(filepath) は一旦コメントアウトするか消します
        # ※ファイルが溜まりすぎないよう、本来は定期的な削除が望ましいです

        # テンプレートに画像パスも渡す
        image_url = url_for('static', filename='uploads/' + filename)
        return render_template("index.html", answer=pred_answer, image_url=image_url)

    return render_template("index.html", answer="", image_url=None)