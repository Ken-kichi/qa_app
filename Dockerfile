# ベースイメージを指定
FROM python:3.11

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコピー
COPY . /app

# pipを更新
RUN pip install --upgrade pip

# openaiを更新
RUN pip install --upgrade openai

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# FLASK_APP環境変数を設定
ENV FLASK_APP=routes.py

# Flaskアプリを起動
CMD ["flask",  "--app=routes", "run", "--host=0.0.0.0"]
