from state import State
from move import Move
from util import validate_pos_int
from game import Game
from game_ended import GameEnded
"""
Represents a game tree that shows all possible trees from
one state, The children of a GameTree are all Games.
A GameTree always has possible moves for at least one player. 
"""

class GameTree(Game):

    def __init__(self, state, children=None):
        """
        Constructor for the Game Tree. Constructs a tree with the given state
        as the current state. Initializes the children of this game tree to empty.
        Children of this GameTree are computed when create_child_trees is called.

        Children is a mapping of possible game actions to their resulting GameTrees and 
        is a recursive data structure that allows possible outcomes of the game to be
        explored. Actions that result in GameTrees are one of a Move (a player moves
        a penguin) or Skip (the player's move is skipped)

        :state: State       The current state within this GameTree
        :children: {Action : GameTree}   Mapping of an Action to resulting GameTree
        :returns: GameTree  Instance of a GameTree
        """
        self.state = state
        self.children = children or {}

    def __eq__(self, other):
        """
        Overrides equality of GameTree, only compare the states.
        Note: If states are equal, then the children will be equal by default
        """
        return type(other) is GameTree and self.state == other.state

    def __ne__(self, other):
        return type(other) is not GameTree and self.state != other.state


    def attempt_move(self, action):
        """
        Attempts the given action on the current state of this game tree and if legal returns the resulting Game.
        Otherwise returns false.
        Side Effect: If the given action is valid, but the child is not in self.children the 
        mapping of Action to Game will be added to children 

        Action -> [Maybe Game]
        """
        if action in self.children:
            return self.children[action]

        maybe_state = action.apply_move(self)
        if maybe_state:
            if maybe_state.any_remaining_moves():
                new_game = GameTree(maybe_state)
            else:
                new_game = GameEnded(maybe_state)
            self.children[action] = new_game
            return new_game
        else:
            return False

    def apply_to_children(self, func):
        """
        Applies the given function to all children of the current game state.

        :func: [GameTree -> X]	Function applied to state's children
        :returns: List of X		List of values returned by func
        """
        new_trees = self.create_child_trees().values()
        moved_trees = list(map(func, new_trees))
        return moved_trees

    def create_child_trees(self):
        """
        Creates a Game for each of this trees children
        If the next player has an Action a GameTree is generated
        If all players have no moves then a GameEnded is generated

        void -> {Action : Game}
        """
        possible_moves = self.state.get_possible_moves()
        for move in possible_moves:
            self.attempt_move(move)
        return self.children

    def get_current_player_color(self):
        return self.state.get_current_player_color()

    def get_players_score(self, player_color):
        return self.state.get_players_score(player_color)

    def create_n_layers_tree(self, num_layers):
        """
        Create N layers of the game decision tree. If num_layers exceeds
        the number of possible turns in the game, return the full tree.

        :num_layers: PositiveInteger    The number of layers to generate
        """
        validate_pos_int(num_layers)
        children = self.create_child_trees()
        if num_layers == 1:
            return self
        else:
            for action in children:
                child_tree = children[action]
                child_tree.create_n_layers_tree(num_layers - 1)
            return self

    def print_children(self):
        if len(self.children) == 0:
            return self.state.print_json()
        arr = []
        for action in self.children:
            arr.append((action.print_json(), self.children[action].print_children()))
        return arr

    def remove_current_player(self):
        """
        Returns the new GameTree created from the state after the current player is removed.

        :returns: GameTree	Resulting GameTree
        """
        new_state = self.state.remove_current_player()
        return GameTree(new_state)

    def has_game_ended(self):
        return not self.state.any_remaining_moves()

    def copy(self):
        state_copy = self.state.copy()
        children_copy = {}
        for action in self.children:
            children_copy[action] = self.children[action].copy()
        return GameTree(state_copy, children_copy)

    def get_winners(self):
        if not self.has_game_ended():
            return False
        return self.state.get_winners()

    def get_possible_actions(self):
        return self.state.get_possible_moves()

    def get_state(self):
        return self.state