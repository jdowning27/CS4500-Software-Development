from operator import le, ge
import os
import sys
os_path = os.path.dirname(os.getcwd()) + '/Fish/Common'
sys.path.append(os_path)

from game_tree import GameTree
from DeadEnd import DeadEnd

def place_penguin_across(state, player_color):
    """
    Places penguin at next available spot.
    The search for the next available spot on the board starts
    in the top left corner and moves across the board from left 
    to right, and down a row when the row is filled.
    Assume that the board is large enough to accommodate all penguins.
    An example of a 4 x 2 board is shown below.

    s = start, tiles numbered in priority order
     ___     ___
    / s \___/ 1 \___
    \___/ 2 \___/ 3 \ 
    / 4 \___/ 5 \___/
    \___/ 6 \___/ 7 \ 
        \___/   \___/
    
    :state: State           The state to place penguins on
    :player_color: Color    The color of the Player to place the penguin for
    
    :returns: State         The state with the penguin placed
    """
    board = state.board
    for row in range(0, board.row):
        for col in range(0, board.col):
            if state.is_tile_available((row, col)):
                return state.place_penguin_for_player(player_color, (row, col))

def choose_action_minimax(tree, num_turns):
    """
    Choose the move for the current player which will return the action
    with the minimal maximum gain for the current player after the given
    number of turns. The minimal maximal gain is quantified by the highest
    possible score for this player, assumming opponents will pick the move
    that minimizes this player's gain.
    If actions result in the same gain, prioritize the penguin whose origin
    has the lowest row, then lowest column index.

    :tree: GameTree                 The tree to search through
    :num_turns: PositiveInteger     Number of turns N > 0 for this player to look through

    :returns: Move                The action this player should take next
    """
    num_players = len(tree.state.players)
    action_score = choose_action_minimax_subtree(tree, (num_turns - 1) * num_players, tree.get_current_player_color())
    return action_score[0]


def choose_action_minimax_subtree(tree, num_turns, max_player):
    """
    Choose the action for the current player in tree that either minimizes
    the max_player's score if it is opponent, or maximizes max_player's score
    if it is their turn

    :tree: GameTree                     The subtree to search through
    :num_turns: PositiveInteger         Number of turns to look through for max_player
    :max_player: Color                  The maximal player's color

    :returns: (Move, Integer)         Where the action is the next action to choose in the tree,
                                        and integer for the score of the max_player
    """
    children = GameTree.create_child_trees(tree)
    if len(children) == 0:
        return (DeadEnd(), tree.get_players_score(max_player))
    elif num_turns == 0:
        max_action_score = (DeadEnd(), 0)
        for action in children:
            child_tree = children[action]
            curr_score = child_tree.get_players_score(max_player)
            if tree.get_current_player_color() is max_player:
                max_action_score = find_minimax_action(max_action_score, (action, curr_score), ge, "called base player")

            else:
                max_action_score = find_minimax_action(max_action_score, (action, curr_score), le, "called base")
        return max_action_score
    else:
        subtree = lambda c : choose_action_minimax_subtree(c, num_turns - 1, max_player)
        list_minimax = GameTree.apply_to_children(tree, subtree)
        printer = lambda x : x.state.print_json()
        print(tree.get_current_player_color(), list_minimax, GameTree.apply_to_children(tree, printer))
        ideal_action_score = (DeadEnd(), 0)
        for action, score in list_minimax:
            if tree.get_current_player_color() is max_player:
                #print("CURRENT PLAYER CHOOSING A MOVE -----   ", num_turns)
                ideal_action_score = find_minimax_action(ideal_action_score, (action, score), ge, "called from this players move")
            else:
                ideal_action_score = find_minimax_action(ideal_action_score, (action, score), le, "called from else")
        return ideal_action_score


def find_minimax_action(ideal_action_score, curr_action_score, comparator, out=""):
    """
    Find the minimax action according to the comparator. Comparator is either
    less than (<) or greater than (>) in order to return either the minimum
    action or the maximum action.

    :ideal_action_score: tuple      (Action, Integer) Move and the resulting score, previous ideal
    :curr_action_score: tuple       (Move, Integer) Move and the resulting score
    :comparator: [Number Number -> Boolean]     Function to compare scores

    :returns: tuple (Move, Integer)       The ideal minimax Move and score
    """
    #print(ideal_action_score)
    ideal_action, ideal_score = ideal_action_score
    curr_action, curr_score = curr_action_score
    if type(ideal_action) is DeadEnd:
        #print("type of ideal_action is DeadEnd")
        return curr_action_score
    if curr_score == ideal_score:
        ideal_action = ideal_action.break_tie(curr_action)
    elif comparator(curr_score, ideal_score):
        
        #print("FOUND a better move")
        ideal_score = curr_score
        ideal_action = curr_action
    return (ideal_action, ideal_score)