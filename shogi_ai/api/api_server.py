from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

# リクエスト/レスポンスのモデル
class InitGameResponse(BaseModel):
    game_id: str

class UpdateBoardRequest(BaseModel):
    game_id: str
    move: str | None = None
    is_vs_myai: bool

class UpdateBoardResponse(BaseModel):
    kifu: str

# 新規対局作成
@app.post("/init-game", response_model=InitGameResponse)
async def init_game():
    game_id = str(uuid.uuid4())
    # posgreSQLにgame_idを保存
    return InitGameResponse(game_id=game_id)

# 盤面更新
@app.post("/update-board", response_model=UpdateBoardResponse)
async def update_board(request: UpdateBoardRequest):
    # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
    # requestのmoveが合法か判断し，盤面を更新
    # 棋譜に手を追加し，posgreSQLに保存
    # 自作のAIを使う場合は，盤面をAIに渡して次の手を取得し，盤面を更新
    # 棋譜に手を追加し，posgreSQLに保存
    return UpdateBoardResponse(kifu="dummy kifu")