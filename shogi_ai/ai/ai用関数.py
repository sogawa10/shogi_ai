# 盤面評価用関数
def evaluate(board):
    pass

# 木探索
def tree_search(board, depth, alpha, beta):
    # 葉ノード
    if depth == 0:
        return evaluate(board)
    if board.is_checkmate(board.turn):
        return float('-inf')
