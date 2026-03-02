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
class RegisterUserRequest(BaseModel):

class RegisterUserResponse(BaseModel):


class GetUserResponse(BaseModel):


class GetUserGamesResponse(BaseModel):


class UpdateUserRequest(BaseModel):

class UpdateUserResponse(BaseModel):


class DeleteUserResponse(BaseModel):


class LoginRequest(BaseModel):

class LoginResponse(BaseModel):


class RegisterAiRequest(BaseModel):

class RegisterAiResponse(BaseModel):


class GetAisResponse(BaseModel):


class UpdateAiRequest(BaseModel):

class UpdateAiResponse(BaseModel):


class DeleteAiResponse(BaseModel):


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


class GetKifuResponse(BaseModel):


class UpdateBoardRequest(BaseModel):
    move: str | None = None

class UpdateBoardResponse(BaseModel):
    kifu: str


class AiMoveRequest(BaseModel):

class AiMoveResponse(BaseModel):
    kifu: str


class EndGameRequest(BaseModel):

class EndGameResponse(BaseModel):



# ユーザー登録
@app.post("/users", response_model=RegisterUserResponse)
def register_user(request: RegisterUserRequest):
    pass

# ユーザー情報を取得
@app.get("/users/{user_name}", response_model=GetUserResponse)
def get_user(user_name: str):
    pass

# 対局を取得
@app.get("/users/{user_id}/games", response_model=GetUserGamesResponse)
def get_user_games(user_id: str):
    pass

# ユーザーを更新
@app.put("/users/{user_id}", response_model=UpdateUserResponse)
def update_user(user_id: str, request: UpdateUserRequest):
    pass

# ユーザーを削除
@app.delete("/users/{user_id}", response_model=DeleteUserResponse)
def delete_user(user_id: str):
    pass

# ログイン
@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    pass

# third-partyのAIを登録
@app.post("/ais", response_model=RegisterAiResponse)
def register_ai(request: RegisterAiRequest):
    pass

# third-partyのAI情報を取得
@app.get("/ais/{ai_name}", response_model=GetAisResponse)
def get_ais(ai_name: str):
    pass

# third-partyのAIを更新
@app.put("/ais/{ai_id}", response_model=UpdateAiResponse)
def update_ai(ai_id: str, request: UpdateAiRequest):
    pass

# third-partyのAIを削除
@app.delete("/ais/{ai_id}", response_model=DeleteAiResponse)
def delete_ai(ai_id: str):
    pass

# 新規対局作成
@app.post("/games", response_model=InitGameResponse)
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

# 棋譜を取得
@app.get("/games/{game_id}/kifu", response_model=GetKifuResponse)
def get_kifu(game_id: str):
    pass

# 盤面更新
@app.post("/games/{game_id}/moves", response_model=UpdateBoardResponse)
def update_board(game_id: str, request: UpdateBoardRequest):
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
@app.post("/games/{game_id}/ai-move", response_model=AiMoveResponse)
def ai_move(game_id: str, request: AiMoveRequest):
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
@app.put("/games/{game_id}", response_model=EndGameResponse)
def end_game(game_id: str, request: EndGameRequest):
    pass
