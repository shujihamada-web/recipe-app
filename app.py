import streamlit as st
import google.generativeai as genai
from PIL import Image

# アプリのタイトルと見た目の設定
st.set_page_config(page_title="冷蔵庫レシピAI", page_icon="🍳")
st.title("🍳 冷蔵庫レシピ提案アプリ")
st.write("冷蔵庫の中身を写真で撮ってアップロードすると、AIがレシピを考えます！")

# 【安全対策】APIキーは画面から入力してもらう
api_key = st.text_input("Gemini APIキーを入力してください（※安全のため画面には隠れて表示されます）", type="password")

# 画像アップロード機能
uploaded_file = st.file_uploader("食材の写真をアップロードしてください (JPG/PNG)", type=["jpg", "png", "jpeg"])

# 画像がアップロードされ、かつAPIキーが入力されている場合のみ実行
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    if api_key:
        if st.button("この食材でレシピを考える！"):
            with st.spinner("AIがレシピを考案中です...🍳"):
                try:
                    # AIの準備
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # AIへの指示
                    prompt = "あなたはプロの料理研究家です。この画像に写っている食材を特定し、それらを使って簡単に作れるレシピを教えてください。" 
                    response = model.generate_content([prompt, image])
                    
                    # 結果の表示
                    st.success("レシピが完成しました！")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("⚠️ まずは上の入力欄にAPIキーを入れてください！")
