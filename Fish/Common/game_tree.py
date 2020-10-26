import State
import Move

"""
Represents a game tree that shows all possible trees from
one state, and has the ability to see to the end.
Includes:
	- Functionality for creating resulting trees from player moves
	- Functionality to apply a function to all child trees
	- Functionality to see the resulting tree from a given action, and legality of this action
"""

class GameTree:

    def __init__(self, state):
        """
        Constructor for the Game Tree. Constructs a tree with the given state
        as the current state. Initializes the children of this game tree to empty

        :state: State       The current state within this GameTree
        :returns: GameTree  Instance of a GameTree
        """
        self.state = state
        self.children = {}

    def __eq__(self, other):
        """
        Overrides equality of GameTree, only compare the states.
        Note: If states are equal, then the children will be equal by default
        """
        return type(other) is GameTree and self.state == other.state

    @staticmethod
    def attempt_move(tree, action):
        """
        Attempts the given action on the state and if legal returns the resulting state.
        Otherwise returns false.

        :tree: GameTree		Origin GameTree to apply action to
        :action: Move		Attempted action

        :returns: maybe GameTree	Resulting GameTree or false
        """
        from_posn = action.get_from_posn()
        to_posn = action.get_to_posn()
        maybe_state = tree.state.move_penguin(from_posn, to_posn)
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
        :returns: Dict {Move : GameTree}
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