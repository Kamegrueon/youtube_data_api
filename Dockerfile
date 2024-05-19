# ベースイメージの指定（ビルドステージ）
FROM python:3.11.7-slim AS builder

ENV APP_HOME=/app
WORKDIR $APP_HOME

# pipとpoetryのインストール
RUN pip install --upgrade pip && pip install poetry

# poetryの依存関係をコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール
RUN poetry export --without-hashes -f requirements.txt > requirements.txt
RUN poetry export --without-hashes --dev -f requirements.txt > requirements-dev.txt
RUN pip install --prefix=/install -r requirements.txt

# 開発依存関係のインストール
RUN pip install --prefix=/install -r requirements-dev.txt

# 本番用の依存関係をコピー
COPY requirements.txt ./

# 開発環境の設定
FROM python:3.11.7-slim AS dev
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# 依存関係のコピー
COPY --from=builder /install /usr/local

# アプリケーションのコードをコピー
COPY src/ ./

# 開発用依存関係のインストール
COPY --from=builder $APP_HOME/requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

# アプリケーションの実行
CMD ["uvicorn", "main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8080"]

# 本番環境の設定
FROM python:3.11.7-slim AS prod
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# 依存関係のコピー
COPY --from=builder /install /usr/local

# アプリケーションのコードをコピー
COPY src/ ./

# アプリケーションの実行
CMD ["uvicorn", "main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8080"]
