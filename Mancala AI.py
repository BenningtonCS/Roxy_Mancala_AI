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
# Player_id, 0 or 1, and board, which is the state of the board. Probably a string.
# The return is the index of the pit to be played in

def random_player(player_id: int, curr_board: [int]) -> int:
    open_spots = get_open_spots(player_id, curr_board)
    return random.choice(open_spots)


def expert_player(player_id: int, curr_board: [int]) -> int:
    scale_factor = player_id * 7
    open_spots = get_open_spots(player_id, curr_board)
    for x in range(5 + scale_factor, -1 + scale_factor, -1):
        if curr_board[x] + x - scale_factor == 6:
            return x  # This prioritizes moves that give extra moves, starting from the pit directly next to the store
        else:  # Here I go three levels deep of moves intended to set up moves that give extra move on subsequent turns
            if curr_board[x] + x - scale_factor == 5:
                return x
            else:  # There's probably a way to make this recur but it's copy/pasted for now
                if curr_board[x] + x - scale_factor == 4:
                    return x
                else:
                    if curr_board[x] + x - scale_factor == 3:
                        return x
                    else:  # Here's the implementation for the opposite side capture choice
                        for y in range(0 + scale_factor, 6 + scale_factor):
                            if (y + curr_board[y]) % 7 < 6:
                                if mancala.opposite_pit(y + curr_board[y]) != 0:
                                    if curr_board[x + y] == 0:
                                        return y
                                    else:
                                        return random.choice(open_spots)


mancala.play_game([mancala.human_player, expert_player], should_display=True, start_player=0)

mancala.run_simulations([expert_player, random_player], 10000, print_statistics=True)
