#!/usr/bin/env python3
# wall.py

__author__ = 'Seth Tinglof'
__version__ = '1.0'


class Wall:
    """
    Wall with a position for player to avoid.
    """

    def __init__(self, horizontal, pos_1, pos_2, pos_3, color):
        """
        Creates a new wall object which players can collide with.  Walls are either horizontal or vertical
        :param horizontal: boolean, true if wall is horizontal and false if vertical.
        :param pos_1: The x position of a vertical wall or the starting x position of a horizontal wall.
        :param pos_2: The starting y position of a vertical wall or the ending x position of a horizontal wall.
        :param pos_3: The ending y position of a vertical wall or the y position of a horizontal wall.
        :param color: The color of the wall
        :return: self
        """
        self.horizontal = horizontal
        if horizontal:
            self.x_pos_1 = pos_1
            self.x_pos_2 = pos_2
            self.y_pos = pos_3
        else:
            self.x_pos = pos_1
            self.y_pos_1 = pos_2
            self.y_pos_2 = pos_3
        self.color = color

    def get_color(self):
        return self.color

    def check_collision(self, player):
        """
        Checks to see if the player passed as an argument has collided with the wall.
        :param player: Player being checked for collision.
        :return: True if player collided, else False.
        """
        if self.horizontal:
            if self.x_pos_1 <= player.get_x_pos() and self.x_pos_2 >= player.get_x_pos() and\
               self.y_pos + 5 >= player.get_y_pos() and self.y_pos - 5 <= player.get_y_pos():
                return True
        else:
            if self.x_pos + 5 >= player.get_x_pos() and self.x_pos - 5 <= player.get_x_pos() and\
               self.y_pos_1 <= player.get_y_pos() and self.y_pos_2 >= player.get_y_pos():
                return True
        return False
