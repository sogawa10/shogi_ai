from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

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
            raise HTTPException(status_code=404, detail="User player not found")
        return result[0]

    elif player_type == "THIRD_PARTY_AI":
        cur.execute("""
            SELECT player_id
            FROM players
            WHERE ai_id = %s
        """, (ai_id,))
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="AI player not found")
        return result[0]

    elif player_type == "FIRST_PARTY_AI":
        cur.execute("""
            SELECT player_id
            FROM players
            WHERE player_type = 'FIRST_PARTY_AI'
        """)
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="AI player not found")
        return result[0]

    else:
        raise HTTPException(status_code=400, detail="Invalid player_type")
    
# アクセストークンを作成
def create_access_token(user_id):
    pass

# アクセストークンを検証
def get_current_user(credentials = Depends(security)):
    pass
