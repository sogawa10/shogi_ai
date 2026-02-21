import os
import uuid
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from psycopg2 import pool

load_dotenv()

# サーバーの起動から停止までのライフスパンを管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時
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
    # 終了時
    app.state.db_pool.closeall()

app = FastAPI(lifespan=lifespan)

# リクエスト/レスポンスのモデル
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

# 新規対局作成
@app.post("/init-game", response_model=InitGameResponse)
def init_game():
    game_id = str(uuid.uuid4())
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLにgame_idを保存
                cur.execute("INSERT INTO games (game_id) VALUES (%s)", (game_id,))
        return InitGameResponse(game_id=game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 盤面更新
@app.post("/update-board", response_model=UpdateBoardResponse)
def update_board(request: UpdateBoardRequest):
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
