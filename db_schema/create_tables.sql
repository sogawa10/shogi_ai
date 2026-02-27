-- usersテーブルを作成
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    user_name VARCHAR(20) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- ai_endpointsテーブルを作成
CREATE TABLE IF NOT EXISTS ai_endpoints (
    ai_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    ai_name VARCHAR(20) NOT NULL,
    full_url TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- playersテーブルを作成
CREATE TABLE IF NOT EXISTS players (
    player_id UUID PRIMARY KEY,
    player_type VARCHAR(20) NOT NULL,
    user_id UUID UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    ai_id UUID UNIQUE REFERENCES ai_endpoints(ai_id) ON DELETE CASCADE
);

-- gamesテーブルを作成
CREATE TABLE IF NOT EXISTS games (
    game_id UUID PRIMARY KEY,
    created_by_user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    sente_player_id UUID REFERENCES players(player_id) ON DELETE CASCADE,
    gote_player_id UUID REFERENCES players(player_id) ON DELETE CASCADE,
    kifu TEXT,
    status VARCHAR(10) NOT NULL,
    result VARCHAR(10),
    created_at TIMESTAMPTZ NOT NULL
);
