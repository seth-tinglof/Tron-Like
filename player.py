#!/usr/bin/env python3
# player.py

__author__ = 'Seth Tinglof'
__version__ = '1.0'


class Player:
    """
    Player class for maze game.  Players are the user controlled characters.
    They have a position and color associated with them.
    """

    MOVE_DISTANCE = 5

    def __init__(self, x_pos, y_pos, color, angle):
        """
        Creates a new player.
        :param x_pos: Starting x position for the player as an integer.
        :param y_pos: Starting y position for the player as an integer.
        :param color: Color of the player as a string.
        :param angle: Starting angle of the player.
        :return: self
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.angle = angle
        self.unhittable_walls = [0, 0]
        self.last_turn_frame = -3

    def get_x_pos(self):
        """
        :return: Player's current x coordinate.
        """
        return self.x_pos

    def get_y_pos(self):
        """
        :return: Player's current y coordinate.
        """
        return self.y_pos

    def get_color(self):
        """
        :return: color of player.
        """
        return self.color

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle

    def move(self):
        """
        Moves player in the direction that they are facing.
        :return: None
        """
        if self.angle == 0:
            self.x_pos += self.MOVE_DISTANCE
        elif self.angle == 90:
            self.y_pos -= self.MOVE_DISTANCE
        elif self.angle == 180:
            self.x_pos -= self.MOVE_DISTANCE
        elif self.angle == 270:
            self.y_pos += self.MOVE_DISTANCE