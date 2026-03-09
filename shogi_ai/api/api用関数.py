import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Bearerトークン認証のヘッダを解析するクラス
security = HTTPBearer()

# player情報を取得する関数
def get_player_id(cur, player_type, user_id, ai_id):
    if player_type == "USER":
        cur.execute("""
            SELECT player_id
            FROM players
            WHERE user_id = %s
        """, (user_id,))
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="⚠ ユーザーが見つかりません。")
        return result[0]

    elif player_type == "THIRD_PARTY_AI":
        cur.execute("""
            SELECT player_id
            FROM players
            WHERE ai_id = %s
        """, (ai_id,))
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="⚠ AIが見つかりません。")
        return result[0]

    elif player_type == "FIRST_PARTY_AI":
        cur.execute("""
            SELECT player_id
            FROM players
            WHERE player_type = 'FIRST_PARTY_AI'
        """)
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="⚠ AIが見つかりません。")
        return result[0]

    else:
        raise HTTPException(status_code=400, detail="⚠ プレイヤーのタイプが不正です。")
    
# アクセストークン（JWT：JSON Web Token）を作成
def create_access_token(user_id):
    # payload = JWTの中に入れるデータ
    exp = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {
        "user_id": user_id,
        "exp": exp
    }
    # JWTを生成
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, exp

# アクセストークンを検証
def get_current_user(credentials = Depends(security)):
    # HTTPヘッダの「Authorization: Bearer <token>」からトークンを取得
    token = credentials.credentials
    # トークンを検証し，user_idを取得
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="⚠ 認証エラーです。 ログインしなおしてください。")
