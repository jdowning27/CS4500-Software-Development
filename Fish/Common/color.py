from enum import Enum

"""
Represents a Player's penguin color.
One color is assigned to each player
"""
class Color(Enum):
    RED = 'red'
    WHITE = 'white'
    BROWN = 'brown'
    BLACK = 'black'
    
    @classmethod
    def get_all_colors(cls):
        return [color for color in Color]
