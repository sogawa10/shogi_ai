-- インデックスを作成
CREATE INDEX IF NOT EXISTS idx_games_sente ON games(sente_player_id);

CREATE INDEX IF NOT EXISTS idx_games_gote ON games(gote_player_id);

CREATE INDEX IF NOT EXISTS idx_games_created_by ON games(created_by_user_id);
