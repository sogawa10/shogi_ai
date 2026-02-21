import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import closing
import uuid
import psycopg2

load_dotenv()

app = FastAPI()

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

# posgreSQLに接続する関数
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

# 新規対局作成
@app.post("/init-game", response_model=InitGameResponse)
def init_game():
    game_id = str(uuid.uuid4())
    conn = None
    try:
        # posgreSQLに接続
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLにgame_idを保存
                cur.execute("INSERT INTO games (game_id) VALUES (%s)", (game_id,))
        return InitGameResponse(game_id=game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

# 盤面更新
@app.post("/update-board", response_model=UpdateBoardResponse)
def update_board(request: UpdateBoardRequest):
    conn = None
    try:
        # posgreSQLに接続
        conn = get_connection()
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
            conn.close()

# first-partyのAIの手を盤面に適応
@app.post("/ai-move", response_model=AiMoveResponse)
def ai_move(request: AiMoveRequest):
    conn = None
    try:
        # posgreSQLに接続
        conn = get_connection()
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
            conn.close()