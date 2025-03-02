# PDFファイル管理アプリのREADME

このアプリは、PDFファイルをアップロード、リスト表示、検索機能を提供します。ユーザーがアップロードしたPDFファイルをデータベースに保存し、ファイルリストを表示します。また、特定のキーワードでPDFファイルを検索し、その内容を表示する機能もあります。

## 使用方法

1. アップロードページにアクセスし、PDFファイルを選択してアップロードします。
2. アップロードされたファイルは、リストページで表示されます。
3. 検索ページで、検索したいキーワードを入力し、検索ボタンをクリックします。
4. 検索結果は、検索ページに表示されます。

## 技術スタック

* Flask: アプリのフレームワーク
* SQLAlchemy: データベースとのやり取り
* OpenAI: 検索機能の実装
* Langchain: 検索機能の実装
* Markdown: マークダウン形式のテキストをHTMLに変換

## 環境変数

* DATABASE_URL: データベースのURL
* OPENAI_KEY: OpenAIのAPIキー

## 実行方法

1. このプロジェクトをクローンします。
2. `docker-compose up` コマンドを実行して、アプリを起動します。
3. ブラウザで `http://localhost:5001` にアクセスします。

## 注意事項

* このアプリは、開発中です。バグや不具合が発生する可能性があります。
* アップロードされたファイルは、サーバーに保存されます。ファイルの内容は、サーバー管理者によってアクセス可能です。
