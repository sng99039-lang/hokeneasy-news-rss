# hokeneasy-news セットアップ手順

## 1. このフォルダの中身をリポジトリにアップロード

リポジトリ作成後、「Add file」→「Upload files」で、このフォルダ内の
以下のファイル・フォルダをそのままドラッグ＆ドロップしてください
（フォルダ構造ごとアップロードされます）。

```
.github/workflows/fetch-news.yml
scripts/fetch_news.py
docs/news.json
docs/index.html
```

## 2. GitHub Pagesを有効化

1. リポジトリの「Settings」タブ
2. 左メニュー「Pages」
3. 「Build and deployment」→ Source: 「Deploy from a branch」
4. Branch: `main` / フォルダ: `/docs` を選択して「Save」
5. 数分待つと、上部に公開URLが表示されます
   （例: `https://ユーザー名.github.io/リポジトリ名/`）

## 3. docs/index.html のURLを書き換える

`docs/index.html` の中の以下の行を、自分のユーザー名・リポジトリ名に書き換えてください。

```js
const NEWS_JSON_URL = 'https://YOUR_USERNAME.github.io/YOUR_REPO/news.json';
```

書き換えたらリポジトリ上でファイルを編集・コミットしてください
（GitHubのWeb画面上で鉛筆マークから直接編集できます）。

## 4. Actionsを手動実行してnews.jsonを生成

1. リポジトリの「Actions」タブ
2. 左メニュー「Fetch Insurance News」
3. 「Run workflow」ボタン→「Run workflow」

1〜2分で完了し、`docs/news.json` に実際のニュースが書き込まれます。
以降は自動で1日4回（6時間おき）更新されます。

## 5. 動作確認

`https://ユーザー名.github.io/リポジトリ名/` にアクセスして、
ニュースが表示されれば成功です。

## 6. Wixに埋め込む

`docs/index.html` の中身（`<script>`まで含めて全部）をコピーして、
Wixの「カスタムHTML」要素に貼り付ければ完了です。
rss2json.comへの依存はなくなり、GitHub Pagesの静的JSONを読むだけなので、
訪問者全員に高速に表示されます。
