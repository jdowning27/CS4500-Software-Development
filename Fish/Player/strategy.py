from operator import le, ge
import math
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

    :returns: Action                The action this player should take next
    """
    num_players = len(tree.state.players)
    layers = num_turns * num_players - (num_players - 1)
    tree.create_n_layers_tree(layers)
    max_player = tree.get_current_player_color()
    action_score = choose_action_minimax_subtree(tree, layers, max_player)
    return action_score[0]


def choose_action_minimax_subtree(tree, num_turns, max_player):
    """
    Choose the action for the current player in tree that either minimizes
    the max_player's score if it is opponent, or maximizes max_player's score
    if it is their turn

    :tree: GameTree                     The tree to search through, child trees should be generated
    :num_turns: Integer                 Number of turns left to take
    :max_player: Color                  The maximal player's color

    :returns: (Action, Integer)         Where the action is the next action to choose in the tree,
                                        and integer for the score of the max_player
    """
    subtree = tree.children

    if len(subtree) == 0:
        tree.create_n_layers_tree(num_turns)
        subtree = tree.children

    if num_turns == 1:
        if tree.get_current_player_color() is max_player:
            ideal_action_score = (None, -math.inf)
            for action in subtree:
                child_tree = subtree[action]
                next_score = child_tree.get_players_score(max_player)
                ideal_action_score = find_minimax_action(ideal_action_score, (action, next_score), ge)
        else:
            ideal_action_score = (None, math.inf)
            for action in subtree:
                child_tree = subtree[action]
                next_score = child_tree.get_players_score(max_player)
                ideal_action_score = find_minimax_action(ideal_action_score, (action, next_score), ge)
        return ideal_action_score
    else:
        list_minimax = []
        for child in subtree:
            child_tree = subtree[child]
            a = choose_action_minimax_subtree(child_tree, num_turns - 1, max_player)
            list_minimax.append((child, a[1]))
        
        ideal_action_score = None
        if tree.get_current_player_color() is max_player:
            ideal_action_score = (None, -math.inf)
            for action, score in list_minimax:
                ideal_action_score = find_minimax_action(ideal_action_score, (action, score), ge)
        else:
            ideal_action_score = (None, math.inf)
            for action, score in list_minimax:
                ideal_action_score = find_minimax_action(ideal_action_score, (action, score), le)
        return ideal_action_score


def find_minimax_action(ideal_action_score, curr_action_score, comparator):
    """
    Find the minimax action according to the comparator. Comparator is either
    less than (<) or greater than (>) in order to return either the minimum
    action or the maximum action.

    :ideal_action_score: tuple      (Action, Integer) Move and the resulting score, previous ideal
    :curr_action_score: tuple       (Move, Integer) Move and the resulting score
    :comparator: [Number Number -> Boolean]     Function to compare scores

    :returns: tuple (Move, Integer)       The ideal minimax Move and score
    """
    ideal_action, ideal_score = ideal_action_score
    if ideal_action is None:
        return curr_action_score
    curr_action, curr_score = curr_action_score
    if curr_score == ideal_score:
        ideal_action = ideal_action.break_tie(curr_action)
    elif comparator(curr_score, ideal_score):
        ideal_score = curr_score
        ideal_action = curr_action
    return (ideal_action, ideal_score)