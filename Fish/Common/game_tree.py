import State
import Move
from Util import validate_pos_int
import Game
"""
Represents a game tree that shows all possible trees from
one state, and has the ability to see to the end.
Includes:
	- Functionality for creating resulting trees from player moves
	- Functionality to apply a function to all child trees
	- Functionality to see the resulting tree from a given action, and legality of this action
"""

class GameTree(Game):

    def __init__(self, state, children={}):
        """
        Constructor for the Game Tree. Constructs a tree with the given state
        as the current state. Initializes the children of this game tree to empty.
        Children of this GameTree are computed when create_child_trees is called.
        Children is a mapping of possible game actions to their resulting GameTrees and 
        is a recursive data structure that allows possible outcomes of the game to be
        explored.

        :state: State       The current state within this GameTree
        :children: {Action : GameTree}   Mapping of an Action to resulting GameTree
        :returns: GameTree  Instance of a GameTree
        """
        self.state = state
        self.children = children

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
        Attempts the given action on the state and if legal returns the resulting state.
        Otherwise returns false.

        :action: Move		Attempted action

        :returns: maybe GameTree	Resulting GameTree or false
        """
        maybe_state = action.apply_move(self)
        if maybe_state:
            return GameTree(maybe_state)
        else:
            return False

    @staticmethod
    def apply_to_children(tree, func):
        """
        Applies the given function to all children of the given state.

        :tree: GameTree			Parent state of children
        :func: [GameTree -> X]	Function applied to state's children
        :returns: List of X		List of values returned by func
        """
        new_trees = GameTree.get_child_trees(tree)
        moved_trees = list(map(func, new_trees))
        return moved_trees

    @staticmethod
    def get_child_trees(tree):
        """
        Gets a list of all the possible direct child trees from the given tree's state.

        :tree: GameTree			    Parent tree, and origin for moves
        :returns: List of GameTree	Children of given tree (resulting GameTree with possible moves)
        """
        possible_moves = tree.state.get_possible_moves()
        new_trees = []
        for move in possible_moves:
            new_trees.append(GameTree.attempt_move(tree, move))
        return new_trees

    @staticmethod
    def create_child_trees(tree):
        """
        Creates game trees for each child state

        :tree: GameTree         The tree to get the child GameTrees for
        :returns: Dict {Action : GameTree}
        """
        possible_moves = tree.state.get_possible_moves()
        for move in possible_moves:
            maybe_tree = GameTree.attempt_move(tree, move)
            if maybe_tree:
                tree.children[move] = maybe_tree
        return tree.children

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
        children = GameTree.create_child_trees(self) 
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
        return self.state.any_remaining_moves()

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
