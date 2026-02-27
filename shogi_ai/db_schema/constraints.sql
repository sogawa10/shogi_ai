-- ai_endpointsテーブルのai_nameに対して，同一ユーザー内での一意性制約を追加
ALTER TABLE ai_endpoints ADD CONSTRAINT ai_name_unique_per_user UNIQUE (
    user_id, ai_name
);

-- playersテーブルのplayer_typeに対して，特定の値のみを許可する制約を追加
ALTER TABLE players ADD CONSTRAINT player_type_value_check CHECK (
    player_type IN ('USER', 'FIRST_PARTY_AI', 'THIRD_PARTY_AI')
);

-- playersテーブルのplayer_typeに基づいた，user_idとai_idの組み合わせの制約を追加
ALTER TABLE players ADD CONSTRAINT player_type_check CHECK (
    (player_type = 'USER' AND user_id IS NOT NULL AND ai_id IS NULL)
 OR (player_type = 'FIRST_PARTY_AI'   AND ai_id IS NULL AND user_id IS NULL)
 OR (player_type = 'THIRD_PARTY_AI' AND ai_id IS NOT NULL AND user_id IS NULL)
);

-- gamesテーブルのstatusに対して，特定の値のみを許可する制約を追加
ALTER TABLE games ADD CONSTRAINT status_value_check CHECK (
    status IN ('PLAYING', 'FINISHED', 'ABORTED')
);

-- gamesテーブルのstatusに基づいた，resultの値の制約を追加
ALTER TABLE games ADD CONSTRAINT status_result_consistency_check CHECK (
    (status = 'PLAYING' AND result IS NULL)
 OR (status = 'ABORTED' AND result IS NULL)
 OR (status = 'FINISHED' AND result IS NOT NULL)
);

-- gamesテーブルのresultに対して，特定の値のみを許可する制約を追加
ALTER TABLE games ADD CONSTRAINT result_value_check CHECK (
    result IN ('SENTE_WIN', 'GOTE_WIN', 'DRAW') OR result IS NULL
);

-- gamesテーブルのsente_player_idとgote_player_idが同一でないことを保証する制約を追加
ALTER TABLE games ADD CONSTRAINT different_players_check CHECK (
    sente_player_id <> gote_player_id
);

-- FIRST_PARTY_AI の初期化
INSERT INTO players (
    player_id,
    player_type
)
VALUES (
    '199f369e-096d-4702-8f32-bb51bbf7c1a8',
    'FIRST_PARTY_AI'
)
ON CONFLICT (player_id) DO NOTHING;
