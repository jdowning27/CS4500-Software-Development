from operator import le, ge
import math

from Fish.Common.game_tree import GameTree
from Fish.Common.game_ended import GameEnded

"""
Represents a strategy to play the game.
This specific strategy places penguins across the game board
at the start of the game, and uses a maximal gain algorithm
to decide moves for the Player that uses this strategy.
"""
class Strategy:

    def place_penguin_across(self, state):
        """
        Places penguin at next available spot.
        The search for the next available spot on the board starts
        in the top left corner and moves across the board from left 
        to right, and down a row when the row is filled.

        Assume that the board is large enough to accommodate all penguins.
        If there are not enough spaces, return False.
        
        An example of a 4 x 2 board is shown below.

        s = start, tiles numbered in priority order
        ___     ___
        / s \___/ 1 \___
        \___/ 2 \___/ 3 \ 
        / 4 \___/ 5 \___/
        \___/ 6 \___/ 7 \ 
            \___/   \___/
        
        :state: State           The state to place penguins on
        
        :returns: [Maybe (int, int)]    Position(row, col) where penguin is placed
        """
        board = state.board
        for row in range(0, board.row):
            for col in range(0, board.col):
                if state.is_tile_available((row, col)):
                    return (row, col)
        return False

    def choose_action_minimax(self, tree, num_turns):
        """
        Choose the move for the current player which will return the action
        with the minimal maximum gain for the current player after the given
        number of turns. The minimal maximal gain is quantified by the highest
        possible score for this player, assumming opponents will pick the move
        that minimizes this player's gain.
        If actions result in the same gain, prioritize the penguin whose origin
        has the lowest row, then lowest column index.
        If there are no valid moves, return a Skip (skipping the current player's turn)

        :tree: GameTree                 The tree to search through
        :num_turns: PositiveInteger     Number of turns N > 0 for this player to look through

        :returns: Action                The action this player should take next
        """
        num_players = len(tree.get_state().players)
        layers = num_turns * num_players
        max_player = tree.get_current_player_color()
        action_score = self.choose_action_minimax_subtree(tree, layers, max_player)
        return action_score[0]


    def choose_action_minimax_subtree(self, tree, num_turns, max_player):
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
        if type(tree) is GameEnded:
            return (None, tree.get_players_score(max_player))
        elif num_turns == 1:
            actions = tree.get_possible_actions()
            if tree.get_current_player_color() is max_player:
                ideal_action_score = (None, -math.inf)
                for action in actions:
                    child_tree = tree.attempt_move(action)
                    next_score = child_tree.get_players_score(max_player)
                    ideal_action_score = self.find_minimax_action(ideal_action_score, (action, next_score), ge)
            else:
                ideal_action_score = (None, math.inf)
                for action in actions:
                    child_tree = tree.attempt_move(action)
                    next_score = child_tree.get_players_score(max_player)
                    ideal_action_score = self.find_minimax_action(ideal_action_score, (action, next_score), le)
            return ideal_action_score
        else:
            actions = tree.get_possible_actions()
            action_scores = []
            for action in actions:
                child = tree.attempt_move(action)
                next_action, score = self.choose_action_minimax_subtree(child, num_turns - 1, max_player)
                action_scores.append((action, score))

            if tree.get_current_player_color() is max_player:
                return self.find_ideal_minimax_action((None, -math.inf), action_scores, ge)
            else:
                return self.find_ideal_minimax_action((None, math.inf), action_scores, le)

    def find_ideal_minimax_action(self, ideal_action_score, action_scores, comparator):
        """
        Abstraction to find the ideal action for the current player who is making a move.
        Either want to maximize or minimize the action depending on the comparator that is 
        passed in. We pick the ideal action, score tuple from the list of action_scores
        
        (Action, Integer) 
        [List-of (Action, Integer)] 
        [Number Number -> Boolean]      -> (Action, Integer)
        """
        curr_ideal = ideal_action_score
        for action, score in action_scores:
            curr_ideal = self.find_minimax_action(curr_ideal, (action, score), comparator)
        return curr_ideal


    def find_minimax_action(self, ideal_action_score, curr_action_score, comparator):
        """
        Find the minimax action according to the comparator. Comparator is either
        less than (<) or greater than (>) in order to return either the minimum
        action or the maximum action.

        :ideal_action_score: tuple      (Action, Integer) Move and the resulting score, previous ideal
        :curr_action_score: tuple       (Move, Integer) Move and the resulting score
        :comparator: [Number Number -> Boolean]     Function to compare scores

        :returns: tuple (Action, Integer)       The ideal minimax Action and score
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
