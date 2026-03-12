from pydantic import BaseModel
from datetime import datetime
from typing import Literal

# リクエスト/レスポンスのモデル
class RegisterUserRequest(BaseModel):
    user_name: str
    password: str

class RegisterUserResponse(BaseModel):
    user_id: str
    player_id: str


class GetUserResponse(BaseModel):
    user_id: str
    user_name: str
    

class GetUserGamesResponse(BaseModel):
    game_id: str
    created_by_user_id: str
    sente_player_type: str
    sente_name: str
    sente_ai_url: str | None
    gote_player_type: str
    gote_name: str
    gote_ai_url: str | None
    kifu: str
    status: Literal["PLAYING", "FINISHED", "ABORTED"]
    result: Literal["SENTE_WIN", "GOTE_WIN", "DRAW"] | None


class GetUserAisResponse(BaseModel):
    ai_id: str
    created_by_user_id: str
    created_by_user_name: str
    ai_name: str
    full_url: str


class UpdateUserRequest(BaseModel):
    user_name: str | None = None
    password: str | None = None

class UpdateUserResponse(BaseModel):
    user_id: str


class LoginRequest(BaseModel):
    user_name: str
    password: str

class LoginResponse(BaseModel):
    user_id: str
    access_token: str
    token_type: str = "bearer"
    exp: datetime


class RegisterAiRequest(BaseModel):
    ai_name: str
    full_url: str

class RegisterAiResponse(BaseModel):
    ai_id: str
    player_id: str


class GetAisResponse(BaseModel):
    ai_id: str
    created_by_user_id: str
    created_by_user_name: str
    ai_name: str
    full_url: str


class UpdateAiRequest(BaseModel):
    ai_name: str | None = None
    full_url: str | None = None

class UpdateAiResponse(BaseModel):
    ai_id: str


class InitGameRequest(BaseModel):
    sente_player_type: Literal["USER", "FIRST_PARTY_AI", "THIRD_PARTY_AI"]
    sente_ai_id: str | None = None
    gote_player_type: Literal["USER", "FIRST_PARTY_AI", "THIRD_PARTY_AI"]
    gote_ai_id: str | None = None

class InitGameResponse(BaseModel):
    game_id: str


class GetGameResponse(BaseModel):
    game_id: str
    created_by_user_id: str
    sente_player_type: str
    sente_name: str
    sente_ai_url: str | None
    gote_player_type: str
    gote_name: str
    gote_ai_url: str | None
    kifu: str
    status: Literal["PLAYING", "FINISHED", "ABORTED"]
    result: Literal["SENTE_WIN", "GOTE_WIN", "DRAW"] | None


class UpdateBoardRequest(BaseModel):
    move: str

class UpdateBoardResponse(BaseModel):
    is_legal_move: bool
    kifu: str
    result: Literal["SENTE_WIN", "GOTE_WIN", "DRAW"] | None = None
    result_type: Literal["CHECKMATE", "NYUGYOKU", "SENNICHITE", "RENZOKU_OTE_SENNICHITE", "MAX_MOVE"] | None = None


class AiMoveResponse(BaseModel):
    kifu: str
    result: Literal["SENTE_WIN", "GOTE_WIN", "DRAW"] | None = None
    result_type: Literal["CHECKMATE", "NYUGYOKU", "SENNICHITE", "RENZOKU_OTE_SENNICHITE", "MAX_MOVE"] | None = None
