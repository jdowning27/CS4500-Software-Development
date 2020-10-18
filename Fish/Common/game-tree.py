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

    def attempt_move(self, state, action):
        """
        Attempts the given action on the state and if legal returns the resulting state.
        Otherwise returns false.

        :state: State		Origin state
        :action: Action		Attempted action

        :returns: maybe State	Resulting state or false
        """
        from_posn = action.get_from_posn()
        to_posn = action.get_to_posn()
        return state.move_penguin(from_posn, to_posn)

    def apply_to_children(self, state, func):
        """
        Applys the given function to all children of the given state.

        :state: State			Parent state of children
        :func: [State -> X]		function applied to state's children
        :returns: List of X		List of values returned by func
        """
        new_states = self.get_child_states(state)
        return map(func, new_states)

    def get_child_states(self, state):
        """
        Gets a list of all the possible direct child states from the given state.

        :state: State			Parent state of states returned
        :returns: List of States	Children of given state
        """
        possible_moves = state.get_possible_moves()
        new_states = []
        for move in possible_moves:
            new_states.append(self.attempt_move(state, possible_move))
        return new_states

    def create_child_trees(self):
        """
        Creates game trees for each child state
        """
        possible_move = self.state.get_possible_moves()
        for move in possible_moves:
            maybe_state = self.attempt_move(self.state, move)
            if maybe_state:
                self.children[move] = GameTree(maybe_state)
        return self.children
