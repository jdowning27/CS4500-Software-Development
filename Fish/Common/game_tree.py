import State
import Action

"""
Represents a a game tree that shows all possible states from
one state and continues til the end.
Includes:
	- Functionality for creating complete tree
	- given state and action if action is legal return resulting state else false
	- Given state and function applies function to all of states immediate children
"""

class GameTree:

    def __init__(self, state):
        self.state = state
        self.children = {}

    def __eq__(self, other):
        return type(other) is GameTree and self.state == other.state

    @staticmethod
    def attempt_move(tree, action):
        """
        Attempts the given action on the state and if legal returns the resulting state.
        Otherwise returns false.

        :tree: GameTree		Origin GameTree to apply action to
        :action: Action		Attempted action

        :returns: maybe State	Resulting state or false
        """
        from_posn = action.get_from_posn()
        to_posn = action.get_to_posn()
        return tree.state.move_penguin(from_posn, to_posn)

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
            new_trees.append(GameTree(GameTree.attempt_move(tree, move)))
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
            maybe_state = GameTree.attempt_move(tree, move)
            if maybe_state:
                tree.children[move] = GameTree(maybe_state)
        return tree.children

