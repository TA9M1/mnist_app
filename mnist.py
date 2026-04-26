from deepface import DeepFace
import os

# 解析したい写真のファイル名に書き換えてください（フォルダ内に置いておく）
target_photo = "test_photo.jpg" 

def test_smile():
    if not os.path.exists(target_photo):
        print(f"エラー: {target_photo} が見つかりません。写真をフォルダに置いてください。")
        return

    print(f"--- {target_photo} を解析中ッ！ ---")
    
    try:
        # DeepFaceで感情分析
        # 初回実行時はモデル（約100MB〜）のダウンロードが自動で始まります
        results = DeepFace.analyze(
            img_path=target_photo, 
            actions=['emotion'],
            enforce_detection=True  # 顔が見つからない場合にエラーを出す設定
        )

        for i, res in enumerate(results):
            score = res['emotion']['happy']
            print(f"一人目（顔 index {i}）の笑顔スコア: {score:.2f}点")
            
            if score > 80:
                print("最高だッ！年賀状確定だッ！")
            else:
                print("もう少し笑顔が欲しいところだぜ…")

    except Exception as e:
        print(f"解析失敗: {e}")

if __name__ == "__main__":
    test_smile()