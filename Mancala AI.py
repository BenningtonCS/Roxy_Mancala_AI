import mancala
import random


def get_open_spots(player_id: int, curr_board: [int]) -> [int]:
    return [x for x in range((0 + (player_id * 7)), (6 + (player_id * 7))) if curr_board[x] != 0]


# Attempt to implement a recursion for the expert AI. Has not yet been tested.
def choice_recur(player_id: int, curr_board: [int], recur_level: int) -> [int]:
    scale_factor = player_id * 7
    while recur_level > 2:
        for x in range(5 + scale_factor, -1 + scale_factor, -1):
            if curr_board[x] + x - scale_factor == recur_level:
                return x
            else:
                choice_recur(player_id, curr_board, recur_level - 1)


# Player functions take two parameters:
# Player_id, 0 or 1, and board, which is the state of the board, which is an array of ints.
# The return is the index of the pit to be played in

def random_player(player_id: int, curr_board: [int]) -> int:
    open_spots = get_open_spots(player_id, curr_board)
    return random.choice(open_spots)


def expert_player(player_id: int, curr_board: [int]) -> int:
    scale_factor = player_id * 7
    open_spots = get_open_spots(player_id, curr_board)
    # player_dish = mancala.player_score_dish (keeping in case it becomes relevant again)
    
    for x in range((5 + scale_factor), (-1 + scale_factor), -1):
        if curr_board[x] + x - scale_factor == 6:
            return x  # This prioritizes moves that give extra moves, starting from the pit directly next to the store
        
        # Here I go three levels deep of moves intended to set up moves that give extra move on subsequent turns
        if curr_board[x] + x - scale_factor == 5:
            return x
        
        # There's probably a way to make this recur but it's copy/pasted for now
        if curr_board[x] + x - scale_factor == 4:
            return x

        # if curr_board[x] + x - scale_factor == 3:
        #    return x
        
    # Here's the implementation for the opposite side capture choice
    # for y in range((0 + scale_factor), (6 + scale_factor)):
    #    if mancala.opposite_pit((y + curr_board[y]) % 7) != 0:
    #        return y
    
    # Return a random choice if all else fails
    return random.choice(open_spots)


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

def minimax_player(player_id : int, curr_board : [int]) -> int:
    open_spots = get_open_spots(player_id, curr_board)
    possible_boards = list(map(lambda x : generate_possible_board(player_id, curr_board, x), open_spots))
    scored_boards = list(map(lambda x : minimax(player_id, x, 9, False), possible_boards))
    
    best_score = max(scored_boards)
    best_moves = [x for x, score in zip(open_spots, scored_boards) if score == best_score]
    return random.choice(best_moves)


# mancala.play_game([minimax_player, mancala.human_player], should_display=True, start_player=0)

print("Minimax vs. Random")
mancala.run_simulations([minimax_player, random_player], 1000, print_statistics=True)

print("Minimax vs. Expert")
mancala.run_simulations([minimax_player, expert_player], 1000, print_statistics=True)

print("Minimax vs. Minimax")
mancala.run_simulations([minimax_player, minimax_player], 1000, print_statistics=True)
