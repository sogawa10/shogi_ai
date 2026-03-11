import os
import uuid
import bcrypt
import psycopg2.extras
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from psycopg2 import pool
from psycopg2.errors import UniqueViolation
from fastapi.middleware.cors import CORSMiddleware
from shogi_ai.api.api用関数 import *
from shogi_ai.api.request_response_model import *
from shogi_ai.対局用.盤面 import 盤面
from shogi_ai.対局用.対局用関数 import *
from shogi_ai.ai.ai import ai_think

load_dotenv()

DEPTH = int(os.getenv("AI_DEPTH"))
origins = os.getenv("ALLOW_ORIGINS")

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ユーザー登録
@app.post("/users", response_model=RegisterUserResponse)
def register_user(request: RegisterUserRequest):
    user_id = uuid.uuid4()
    password_hash = bcrypt.hashpw(
        request.password.encode(),
        bcrypt.gensalt()
        ).decode()
    player_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLにユーザー情報を保存
                cur.execute("""
                    INSERT INTO users (
                        user_id,
                        user_name,
                        password_hash,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                """, (user_id, request.user_name, password_hash, now, now))
                # posgreSQLにプレーヤー情報を保存
                cur.execute("""
                    INSERT INTO players (
                        player_id,
                        player_type,
                        user_id
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    );
                """, (player_id, "USER", user_id))
        return RegisterUserResponse(user_id=str(user_id), player_id=str(player_id))
    except HTTPException:
        raise
    except UniqueViolation:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="⚠ このユーザー名は既に使用されています。"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# ユーザー情報を取得
@app.get("/users/me", response_model=GetUserResponse)
def get_user(user_id: str = Depends(get_current_user)):
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLからユーザー情報を取得
                cur.execute("""
                    SELECT user_id, user_name 
                    FROM users
                    WHERE user_id = %s;
                """, (user_id,))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="⚠ ユーザーが見つかりません。")
        return GetUserResponse(user_id=str(result[0]), user_name=result[1])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 対局を取得
@app.get("/users/me/games", response_model=list[GetUserGamesResponse])
def get_user_games(user_id: str = Depends(get_current_user)):
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                 # posgreSQLから対局情報を取得
                cur.execute("""
                    SELECT game_id, created_by_user_id, sente_player_id, gote_player_id, kifu, status, result
                    FROM games
                    WHERE created_by_user_id = %s;
                """, (user_id,))
                results = cur.fetchall()
        return [
            GetUserGamesResponse(game_id=str(r[0]), created_by_user_id=str(r[1]), sente_player_id=str(r[2]), gote_player_id=str(r[3]), kifu=r[4], status=r[5], result=r[6])
            for r in results
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# third-partyのAI情報を取得（ユーザーIDによる検索）
@app.get("/users/me/ais", response_model=list[GetUserAisResponse])
def get_user_ais(user_id: str = Depends(get_current_user)):
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                 # posgreSQLからAI情報を取得
                cur.execute("""
                    SELECT 
                        a.ai_id,
                        a.user_id,
                        u.user_name,
                        a.ai_name,
                        a.full_url
                    FROM ai_endpoints a
                    JOIN users u
                        ON a.user_id = u.user_id
                    WHERE a.user_id = %s;
                """, (user_id,))
                results = cur.fetchall()
        return [
            GetUserAisResponse(ai_id=str(r[0]), created_by_user_id=str(r[1]), created_by_user_name=str(r[2]), ai_name=str(r[3]), full_url=str(r[4]))
            for r in results
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# ユーザーを更新
@app.put("/users/me", response_model=UpdateUserResponse)
def update_user(request: UpdateUserRequest, user_id: str = Depends(get_current_user)):
    if request.user_name is None and request.password is None:
        raise HTTPException(status_code=400, detail="⚠ 変更された項目がありません。")
    if request.password is not None:
        password_hash = bcrypt.hashpw(
            request.password.encode(),
            bcrypt.gensalt()
            ).decode()
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQL内のユーザー情報を修正
                if request.user_name is not None and request.password is not None:
                    cur.execute("""
                        UPDATE users
                        SET user_name = %s,
                            password_hash = %s,
                            updated_at = %s
                        WHERE user_id = %s;
                    """, (request.user_name, password_hash, now, user_id))
                elif request.user_name is not None:
                    cur.execute("""
                        UPDATE users
                        SET user_name = %s,
                            updated_at = %s
                        WHERE user_id = %s;
                    """, (request.user_name, now, user_id))
                elif request.password is not None:
                    cur.execute("""
                        UPDATE users
                        SET password_hash = %s,
                            updated_at = %s
                        WHERE user_id = %s;
                    """, (password_hash, now, user_id))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="⚠ ユーザーが見つかりません。")
        return UpdateUserResponse(user_id=str(user_id))
    except HTTPException:
        raise
    except UniqueViolation:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="⚠ このユーザー名は既に使用されています。"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# ログイン
@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLからユーザー情報を取得
                cur.execute("""
                    SELECT user_id, password_hash
                    FROM users
                    WHERE user_name = %s;
                """, (request.user_name,))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=401, detail="⚠ ユーザー名またはパスワードが正しくありません。")
                user_id, password_hash = result
                # パスワードを検証
                if not bcrypt.checkpw(request.password.encode(), password_hash.encode()):
                    raise HTTPException(status_code=401, detail="⚠ ユーザー名またはパスワードが正しくありません。")
                # アクセストークンを作成
                access_token, exp = create_access_token(str(user_id))

        return LoginResponse(user_id=str(user_id), access_token=access_token, exp=exp)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# third-partyのAIを登録
@app.post("/ais", response_model=RegisterAiResponse)
def register_ai(request: RegisterAiRequest, user_id: str = Depends(get_current_user)):
    ai_id = uuid.uuid4()
    player_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLにAI情報を保存
                cur.execute("""
                    INSERT INTO ai_endpoints (
                        ai_id,
                        user_id,
                        ai_name,
                        full_url,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                """, (ai_id, user_id, request.ai_name, request.full_url, now, now))
                # posgreSQLにプレーヤー情報を保存
                cur.execute("""
                    INSERT INTO players (
                        player_id,
                        player_type,
                        ai_id
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    );
                """, (player_id, "THIRD_PARTY_AI", ai_id))
        return RegisterAiResponse(ai_id=str(ai_id), player_id=str(player_id))
    except HTTPException:
        raise
    except UniqueViolation:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="⚠ このAIは既に存在しています。"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# third-partyのAI情報を取得（名前検索）
@app.get("/ais/{ai_name}", response_model=list[GetAisResponse])
def get_ais(ai_name: str, user_id: str = Depends(get_current_user)):
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                 # posgreSQLからAI情報を取得
                cur.execute("""
                    SELECT 
                        a.ai_id,
                        a.user_id,
                        u.user_name,
                        a.ai_name,
                        a.full_url
                    FROM ai_endpoints a
                    JOIN users u
                        ON a.user_id = u.user_id
                    WHERE a.ai_name = %s;
                """, (ai_name,))
                results = cur.fetchall()
        return [
            GetUserAisResponse(ai_id=str(r[0]), created_by_user_id=str(r[1]), created_by_user_name=str(r[2]), ai_name=str(r[3]), full_url=str(r[4]))
            for r in results
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# third-partyのAIを更新
@app.put("/ais/{ai_id}", response_model=UpdateAiResponse)
def update_ai(request: UpdateAiRequest, ai_id: str, user_id: str = Depends(get_current_user)):
    if request.ai_name is None and request.full_url is None:
        raise HTTPException(status_code=400, detail="⚠ 変更された項目がありません。")
    now = datetime.now(timezone.utc)
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQL内のAI情報を修正
                if request.ai_name is not None and request.full_url is not None:
                    cur.execute("""
                        UPDATE ai_endpoints
                        SET ai_name = %s,
                            full_url = %s,
                            updated_at = %s
                        WHERE ai_id = %s
                        AND user_id = %s;
                    """, (request.ai_name, request.full_url, now, ai_id, user_id))
                elif request.ai_name is not None:
                    cur.execute("""
                        UPDATE ai_endpoints
                        SET ai_name = %s,
                            updated_at = %s
                        WHERE ai_id = %s
                        AND user_id = %s;
                    """, (request.ai_name, now, ai_id, user_id))
                elif request.full_url is not None:
                    cur.execute("""
                        UPDATE ai_endpoints
                        SET full_url = %s,
                            updated_at = %s
                        WHERE ai_id = %s
                        AND user_id = %s;
                    """, (request.full_url, now, ai_id, user_id))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="⚠ AIが見つかりません。")
        return UpdateAiResponse(ai_id=str(ai_id))
    except HTTPException:
        raise
    except UniqueViolation:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="⚠ このAIは既に存在しています。"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 新規対局作成
@app.post("/games", response_model=InitGameResponse)
def init_game(request: InitGameRequest, user_id: str = Depends(get_current_user)):
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
                # posgreSQLに対局情報を保存
                cur.execute("""
                    INSERT INTO games (
                        game_id,
                        created_by_user_id,
                        sente_player_id,
                        gote_player_id,
                        kifu,
                        status,
                        created_at
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                """, (game_id, user_id, sente_player_id, gote_player_id, "", "PLAYING", now))
        return InitGameResponse(game_id=str(game_id))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 棋譜を取得
@app.get("/games/{game_id}/kifu", response_model=GetKifuResponse)
def get_kifu(game_id: str, user_id: str = Depends(get_current_user)):
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLから棋譜を取得
                cur.execute("""
                    SELECT kifu
                    FROM games
                    WHERE game_id = %s
                    AND created_by_user_id = %s;
                """, (game_id, user_id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="⚠ 棋譜が見つかりません。")
        return GetKifuResponse(kifu=result[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# 盤面更新
@app.post("/games/{game_id}/moves", response_model=UpdateBoardResponse)
def update_board(request: UpdateBoardRequest, game_id: str, user_id: str = Depends(get_current_user)):
    board = 盤面()
    is_legal_move = False
    status = "PLAYING"
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
                cur.execute("""
                    SELECT kifu
                    FROM games
                    WHERE game_id = %s
                    AND created_by_user_id = %s
                    FOR UPDATE;
                """, (game_id, user_id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="⚠ 対局が見つかりません。")
                kifu = result[0]
                position_history, position_sequence = board.load_kifu(kifu)
                move = request.move
                now_move = move2te(move, board)
                if now_move is None:
                    return UpdateBoardResponse(is_legal_move=False, kifu=kifu)
                # 盤面の合法手を生成する
                board_moves = board.generate_board_moves(board.turn)
                uchite = board.generate_uchite(board.turn)
                legal_moves = board.filter_shogi_rules(board_moves, uchite)
                # 入力された手が合法手かどうか確認する
                for legal_move in legal_moves:
                    if (
                        type(legal_move.koma) is type(now_move.koma)
                        and legal_move.from_pos == now_move.from_pos
                        and legal_move.to_pos == now_move.to_pos
                        and legal_move.nari == now_move.nari
                        and legal_move.uchite == now_move.uchite
                    ):
                        is_legal_move = True
                        break
                if not is_legal_move:
                    return UpdateBoardResponse(is_legal_move=is_legal_move, kifu=kifu)
                # 手を盤面に適応
                history = board.apply_move(now_move)
                game_result, game_result_type = check_game_end(board, position_history, position_sequence)
                if game_result:
                    status = "FINISHED"
                # 棋譜に手を追加し，posgreSQLに保存
                kifu = (kifu + " " + move).strip()
                cur.execute("""
                    UPDATE games
                    SET kifu = %s, status = %s, result = %s
                    WHERE game_id = %s
                    AND created_by_user_id = %s
                    AND status = %s
                """, (kifu, status, game_result, game_id, user_id, "PLAYING"))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="⚠ 対局が見つかりません。")
        return UpdateBoardResponse(is_legal_move=is_legal_move, kifu=kifu, result=game_result, result_type=game_result_type)
    except HTTPException:
        raise
    except Exception as e:
        # エラー時にABORTEDする
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE games
                        SET status = 'ABORTED'
                        WHERE game_id = %s
                        AND created_by_user_id = %s
                        AND status = %s;
                    """, (game_id, user_id, "PLAYING"))
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)

# first-partyのAIの手を盤面に適応
@app.post("/games/{game_id}/ai-move", response_model=AiMoveResponse)
def ai_move(game_id: str, user_id: str = Depends(get_current_user)):
    board = 盤面()
    status = "PLAYING"
    conn = None
    try:
        # posgreSQLに接続
        conn = app.state.db_pool.getconn()
        with conn:
            with conn.cursor() as cur:
                # posgreSQLからgame_idに対応する棋譜を取得し，盤面を復元
                cur.execute("""
                    SELECT kifu
                    FROM games
                    WHERE game_id = %s
                    AND created_by_user_id = %s
                    FOR UPDATE;
                """, (game_id, user_id))
                result = cur.fetchone()
                if result is None:
                    raise HTTPException(status_code=404, detail="⚠ 対局が見つかりません。")
                kifu = result[0]
                position_history, position_sequence = board.load_kifu(kifu)
                # 盤面をAIに渡して次の手を取得し，盤面を更新
                ai_move = ai_think(board, DEPTH)
                move = ai_move.to_string()
                history = board.apply_move(ai_move)
                game_result, game_result_type = check_game_end(board, position_history, position_sequence)
                if game_result:
                    status = "FINISHED"
                # 棋譜に手を追加し，posgreSQLに保存
                kifu = (kifu + " " + move).strip()
                cur.execute("""
                    UPDATE games
                    SET kifu = %s, status = %s, result = %s
                    WHERE game_id = %s
                    AND created_by_user_id = %s
                    AND status = %s
                """, (kifu, status, game_result, game_id, user_id, "PLAYING"))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="⚠ 対局が見つかりません。")
        return AiMoveResponse(kifu=kifu, result=game_result, result_type=game_result_type)
    except HTTPException:
        raise
    except Exception as e:
        # エラー時にABORTEDする
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE games
                        SET status = 'ABORTED'
                        WHERE game_id = %s
                        AND created_by_user_id = %s
                        AND status = %s;
                    """, (game_id, user_id, "PLAYING"))
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            app.state.db_pool.putconn(conn)
