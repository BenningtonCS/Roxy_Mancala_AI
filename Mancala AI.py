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
    for y in range((0 + scale_factor), (6 + scale_factor)):
        if mancala.opposite_pit((y + curr_board[y]) % 7) != 0:
            return y
    
    # Return a random choice if all else fails
    return random.choice(open_spots)


# mancala.play_game([expert_player, mancala.human_player], should_display=True, start_player=0)

mancala.run_simulations([expert_player, random_player], 10000, print_statistics=True)
