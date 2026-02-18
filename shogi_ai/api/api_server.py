import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
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

# 新規対局作成
@app.get("/init-game", response_model=InitGameResponse)
async def init_game():
    game_id = str(uuid.uuid4())
    # posgreSQLに接続
    conn = psycopg2.connect(
        host=os.getenv("DB_NAME"),
        detabase=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    # posgreSQLにgame_idを保存
    cur.execute("SQL文をここに記述")
    conn.commit()
    cur.close()
    conn.close()
    return InitGameResponse(game_id=game_id)

# 盤面更新
@app.post("/update-board", response_model=UpdateBoardResponse)
async def update_board(request: UpdateBoardRequest):
    # posgreSQLに接続
    conn = psycopg2.connect(
        host=os.getenv("DB_NAME"),
        detabase=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
    cur.execute("SQL文をここに記述")
    result = cur.fetchone()
    # requestのmoveが合法か判断し，盤面を更新
    # 棋譜に手を追加し，posgreSQLに保存
    cur.execute("SQL文をここに記述")
    conn.commit()
    cur.close()
    conn.close()
    return UpdateBoardResponse(kifu="dummy kifu")

# first-partyのAIの手を盤面に適応
@app.post("/ai-move", response_model=AiMoveResponse)
async def ai_move(request: AiMoveRequest):
    # posgreSQLに接続
    conn = psycopg2.connect(
        host=os.getenv("DB_NAME"),
        detabase=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
    cur.execute("SQL文をここに記述")
    result = cur.fetchone()
    # 盤面をAIに渡して次の手を取得し，盤面を更新
    # 棋譜に手を追加し，posgreSQLに保存
    cur.execute("SQL文をここに記述")
    conn.commit()
    cur.close()
    conn.close()
    return AiMoveResponse(kifu="dummy kifu")