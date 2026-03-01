import os
import uuid
import psycopg2.extras
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from psycopg2 import pool
from shogi_ai.api.api用関数 import *

load_dotenv()

# サーバーの起動から停止までのライフスパンを管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時（UUIDをpsycopg2で扱えるようにしたうえで，データベースプールの初期化を行う）
    psycopg2.extras.register_uuid()
    app.state.db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    # サーバー稼働中
    yield
    # 終了時（データベースプールを閉じる）
    app.state.db_pool.closeall()

app = FastAPI(lifespan=lifespan)

# リクエスト/レスポンスのモデル
class InitGameRequest(BaseModel):
    created_by_user_id: str
    sente_player_type: str
    sente_user_id: str | None = None
    sente_ai_id: str | None = None
    gote_player_type: str
    gote_user_id: str | None = None
    gote_ai_id: str | None = None

class InitGameResponse(BaseModel):
    game_id: str

class UpdateBoardRequest(BaseModel):
    game_id: str
    move: str | None = None

class UpdateBoardResponse(BaseModel):
    kifu: str

class AiMoveRequest(BaseModel):
    game_id: str


class AiMoveResponse(BaseModel):
    kifu: str

# ユーザー登録
@app.post("/register-user")
def register_user():
    pass

# ユーザー情報を取得
@app.get("/get-user/{user_name}")
def get_user(user_name: str):
    pass

# ユーザーを更新
@app.post("/update-user")
def update_user():
    pass

# ユーザーを削除
@app.delete("/delete-user")
def delete_user():
    pass

# ログイン
@app.post("/login")
def login():
    pass

# third-partyのAIを登録
@app.post("/register-ai")
def register_ai():
    pass

# third-partyのAI情報を取得
@app.get("/get-ai/{ai_name}")
def get_ai(ai_name: str):
    pass

# third-partyのAIを更新
@app.post("/update-ai")
def update_ai():
    pass

# third-partyのAIを削除
@app.delete("/delete-ai")
def delete_ai():
    pass

# 新規対局作成
@app.post("/init-game", response_model=InitGameResponse)
def init_game(request: InitGameRequest):
    game_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                sente_player_id = get_player_id(cur, request.sente_player_type, request.sente_user_id, request.sente_ai_id)
                gote_player_id = get_player_id(cur, request.gote_player_type, request.gote_user_id, request.gote_ai_id)
                # posgreSQLにgame_idを保存
                cur.execute("""
                    INSERT INTO games (
                        game_id,
                        created_by_user_id,
                        sente_player_id,
                        gote_player_id,
                        status,
                        created_at
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (game_id) DO NOTHING;
                """, (game_id, request.created_by_user_id, sente_player_id, gote_player_id, "PLAYING", now))
        return InitGameResponse(game_id=str(game_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 対局を取得
@app.get("/get-game/{user_id}")
def get_game(user_id: str):
    pass

# 棋譜を取得
@app.get("/get-kifu/{game_id}")
def get_kifu(game_id: str):
    pass

# 盤面更新
@app.post("/update-board", response_model=UpdateBoardResponse)
def update_board(request: UpdateBoardRequest):
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
                cur.execute("SQL文をここに記述")
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Game not found")
                # requestのmoveが合法か判断し，盤面を更新
                # 棋譜に手を追加し，posgreSQLに保存
                cur.execute("SQL文をここに記述")
        return UpdateBoardResponse(kifu="dummy kifu")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# first-partyのAIの手を盤面に適応
@app.post("/ai-move", response_model=AiMoveResponse)
def ai_move(request: AiMoveRequest):
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
                cur.execute("SQL文をここに記述")
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="Game not found")
                # 盤面をAIに渡して次の手を取得し，盤面を更新
                # 棋譜に手を追加し，posgreSQLに保存
                cur.execute("SQL文をここに記述")
        return AiMoveResponse(kifu="dummy kifu")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 対局を終了
@app.post("/end-game")
def end_game():
    pass
