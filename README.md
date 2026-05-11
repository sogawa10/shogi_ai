# 将棋AI (shogi_ai)

## 概要

本プロジェクトは，将棋AIを自前実装することを目的とした学習用プロジェクトです．**将棋のルール処理および状態管理機能**，**AI機能**，そして**GUI機能**を段階的に実装します．既存の将棋エンジンを使用することなく，基礎構造から実装している点が特徴です．

将棋のルールとして，**二歩の禁止**，**行き所のない駒の禁止**，**打ち歩詰めの禁止**，**千日手判定**，**入玉宣言法**を実装しました．

本プロジェクトで実装したAPIおよびAI機能を用いて，将棋AI対局Webサイトを実装するプロジェクトはこちらです（[shogi-frontend](https://github.com/sogawa10/shogi_frontend)）．

## 必要なライブラリとソフトウェア

### 本プロジェクトを動かすためには、以下のライブラリが必要です．

- python-dotenv
- fastapi
- uvicorn
- pydantic
- psycopg2
- bcrypt
- python-jose

### 本プロジェクトを動かすためには、以下のソフトウェアが必要です．

- postgresql

## プロジェクト内のディレクトリ構成

1. db_schemaフォルダ\
   → **データベースのスキーマ**を記述したsqlファイル群．実行されると，DBが初期化される．
2. shogi_aiフォルダ\
   → **将棋のルール処理および状態管理機能**，**AI機能**，そして**API機能**のためのpythonコード群．コマンドライン上での対局およびAPIサーバーの起動を行うことができる．
3. .env\
   → 環境変数設定ファイル．GitHubにはアップロードされない．
4. .gitignore\
   → GitHubにアップロードしたくないファイルを記述する．

## 使い方

### コマンドライン上で対局を行う場合は，以下を参考にしてください．

1. 次の対局スクリプトを直接実行することで，人間同士の対戦や，人間対AIの対戦を行うことができます．\
`python -m shogi_ai`
2. 駒を動かしたい場合は，**「5453」** のように，元居る場所の x座標，y座標，進みたい場所の x座標，y座標 を入力してください．成りたい場合は，**「5453成」** のように，最後に「成」と追加してください．
3. 駒を打ちたい場合は，**「歩55」** のように，打ちたい駒の名前と，進みたい場所の x座標，y座標 を入力してください．

### APIサーバーを起動する際は，以下のコマンドを入力してください．
`uvicorn shogi_ai.api.api_server:app --reload`

## システムの全体像

![Image](https://github.com/user-attachments/assets/6f1ec107-2347-49db-ae23-745df532a6e7)

## データベースの構造

![Image](https://github.com/user-attachments/assets/8babc227-a45f-42f0-b501-ce0135570fea)

### ER図の属性については，以下を参考にしてください．

1. **users** (ユーザー情報を管理)
   - user_id\
   → ユーザー固有のID．
   - user_name\
   → 一意となる，ユーザー固有のログインID．
   - password_hash\
    → パスワードをハッシュ値として保存．
   - created_at\
   → レコードが作成された日時．
   - updated_at\
   → レコードが最後に更新された日時．
2. **ai_endpoints** (third-partyの将棋AIを管理)
   - ai_id\
   → 将棋AI固有のID．
   - user_id\
   → どのユーザーが作成した将棋AIかを判別．
   - ai_name\
   → 同一ユーザー内で一意となるAIの名称．
   - full_url\
   → 将棋AI(API)を呼び出すURL．
   - created_at\
   → レコードが作成された日時．
   - updated_at\
   → レコードが最後に更新された日時．
3. **players** (ユーザーとAIを対局で扱える形で管理)
   - player_id\
   → プレーヤー固有のID．
   - player_type\
   → プレーヤーの種別．\
   → USER・FIRST_PARTY_AI・THIRD_PARTY_AI のいずれか．
   - user_id\
   → プレーヤーの種別がUSERの場合に，どのユーザーかを識別．
   - ai_id\
   → プレーヤーの種別がTHIRD_PARTY_AIの場合に，どの将棋AIかを識別．
4. **games** (対局情報を管理)
   - game_id\
   → 対局固有のID．
   - created_by_user_id\
   → 対局を作成したユーザーのID．
   - sente_player_id\
   → 先手番のプレーヤーID．
   - gote_player_id\
   → 後手番のプレーヤーID．
   - kifu\
   → 後述のAPIの仕様に則った形式の棋譜情報．
   - status\
   → 対局の進行状態．\
   → PLAYING・FINISHED・ABORTED のいずれか．
   - result\
   → 対局の結果．\
   → SENTE_WIN・GOTE_WIN・DRAW・NULL のいずれか．
   - created_at\
   → レコードが作成された日時．
   - updated_at\
   → レコードが最後に更新された日時．

### PostgreSQLでデータベースを構築する際は，以下を参考にしてください．

1. 管理者ユーザーである**postgres**でRDBMSにログインする．\
`psql -U postgres`
2. ログイン後，**データベース**や**ユーザー**を作成する．\
`CREATE USER ユーザー名 WITH PASSWORD 'パスワード';`\
`CREATE DATABASE データベース名 OWNER ユーザー名;`
3. 一度ログアウトして，SQLファイル（constraints.sqlと，create_tables.sqlと，indexes.sql）をもとにDBを構築する．\
`psql -U ユーザー名 -d データベース名 -f db_schema/create_tables.sql`\
`psql -U ユーザー名 -d データベース名 -f db_schema/constraints.sql`\
`psql -U ユーザー名 -d データベース名 -f db_schema/indexes.sql`
4. 一度ログアウトして，作成したデータベースに，作成したユーザーでログインする．\
`psql -U ユーザー名 -d データベース名`

## ライセンス

本プロジェクトは，MITライセンスの下でライセンスされています．
