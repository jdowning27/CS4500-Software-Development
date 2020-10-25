from Action import Action

class DeadEnd(Action):

    def break_tie(self, other):
        return other