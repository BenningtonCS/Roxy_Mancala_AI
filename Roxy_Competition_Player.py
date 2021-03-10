import random
import mancala


def get_open_spots(player_id: int, curr_board: [int]) -> [int]:
    return [x for x in range((0 + (player_id * 7)), (6 + (player_id * 7))) if curr_board[x] != 0]


def score_board(player_id : int, board : [int]) -> int:
    # Takes the scores of each player and returns the difference between the player's and opponent's score.
    # This should allow minimax to prioritize boards which both maximize the player's score and minimize the opponent's score.
    # I'm currently wondering if there is an approach where both scores and not the difference is more useful.
    player_score = mancala.get_score(player_id, board)
    opponent_score = mancala.get_score(mancala.get_opponent_id(player_id), board)
    return (player_score - opponent_score)


def generate_possible_board(player_id : int, curr_board : [int], spot_to_play : int) -> [int]:
    # mancala.sow() returns two variables but we only need the second one. Maybe this isn't the right function to use,
    # but it seemed to be what would update a board one move.
    next_player, next_board = mancala.sow(spot_to_play, player_id, curr_board)
    return next_board

    
def minimax(player_id : int, curr_board : [int], depth : int, should_maximize : bool) -> int:
    open_spots = get_open_spots(player_id, curr_board)
    curr_score = score_board(player_id, curr_board)
    is_game_over = mancala.game_is_over(curr_board)
    
    alpha = float('-inf')
    beta = float('inf')
    
    # Stop recurring if we've reached maximum depth or the game is over.
    # game_is_over from the header file is used to determine the latter.
    if depth == 0 or is_game_over == 0:
        return curr_score * (depth + 1)
    
    if should_maximize:
        max_score = float('-inf')
        for spot in open_spots:
            board = generate_possible_board(player_id, curr_board, spot)
            score = minimax(player_id, board, depth - 1, False)
            max_score = max(max_score, score)
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score
    else:
        min_score = float('inf')
        for spot in open_spots:
            board = generate_possible_board(mancala.get_opponent_id(player_id), curr_board, spot)
            score = minimax(player_id, board, depth - 1, True)
            min_score = min(min_score, score)
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return min_score

    
def competition_player(player_id : int, curr_board : [int]) -> int:
    open_spots = get_open_spots(player_id, curr_board)
    possible_boards = list(map(lambda x : generate_possible_board(player_id, curr_board, x), open_spots))
    scored_boards = list(map(lambda x : minimax(player_id, x, 5, False), possible_boards))
    
    best_score = max(scored_boards)
    best_moves = [x for x, score in zip(open_spots, scored_boards) if score == best_score]
    return random.choice(best_moves)

