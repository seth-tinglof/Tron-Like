#!/usr/bin/env python3
# window.py

from tkinter import *

__author__ = 'Seth Tinglof'
__version__ = '1.0'


class Window:

    SIZE_X = 1280
    SIZE_Y = 720

    def __init__(self, characters, walls):
        """
        Window for maze game.  Displays a character and walls for the character to avoid.
        :param characters: characters displayed on screen.  Should be a list even if only one is used.
        :param walls: Walls displayed on screen.  Should be a list
        :return: None
        """
        self.characters = characters
        self.walls = walls
        self.blue_score = 0
        self.red_score = 0

        # Master
        self.root = Tk()
        self.root.title("Maze")

        # Frame Setup
        self.center_frame = Frame(self.root)
        self.intro_frame = Frame(self.root)

        # Canvas Setup
        self.canvas = Canvas(self.center_frame, width=self.SIZE_X, height=self.SIZE_Y)
        self.intro_canvas = Canvas(self.intro_frame, width=self.SIZE_X, height=self.SIZE_Y)
        self.intro_image = None
        self.canvas.pack()

        # Buttons
        self.play_button = Button(self.intro_frame)
        self.play_button["text"] = "Play"
        self.play_button.pack(side='bottom')

    def update_canvas(self):
        """
        Updates canvas to reflect current positions.
        :return: None
        """
        self.canvas.delete(ALL)

        for character in self.characters:
            self.canvas.create_rectangle(character.get_x_pos() - 5, character.get_y_pos() - 5, character.get_x_pos() + 5,
                                         character.get_y_pos() + 5, fill=character.get_color())

        for wall in self.walls:
            if wall.horizontal:
                self.canvas.create_rectangle(wall.x_pos_1 - 5, wall.y_pos + 5, wall.x_pos_2 + 5, wall.y_pos - 5,
                                             fill=wall.get_color(), outline=wall.get_color())
            else:
                self.canvas.create_rectangle(wall.x_pos + 5, wall.y_pos_1 + 5, wall.x_pos - 5, wall.y_pos_2 - 5,
                                             fill=wall.get_color(), outline=wall.get_color())

        self.canvas.create_text(150, 50, text=str("Blue Score:"), font=("Times", "48"))
        self.canvas.create_text(170, 100, text=str(self.blue_score), font=("Times", "36"))
        self.canvas.create_text(1100, 50, text=str("Red Score:"), font=("Times", "48"))
        self.canvas.create_text(1150, 100, text=str(self.red_score), font=("Times", "36"))
        self.canvas.update()

    def intro(self):
        self.intro_image = PhotoImage(file="intro.gif")
        self.intro_frame.pack()
        self.play_button.pack()
        self.intro_canvas.pack()
        self.intro_canvas.delete(ALL)
        self.intro_canvas.create_image(0, 0, image=self.intro_image, anchor=NW)
        self.intro_canvas.update()

    def set_score(self, blue_score, red_score):
        self.blue_score = blue_score
        self.red_score = red_score
