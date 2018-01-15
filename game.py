#!/usr/bin/env python3
# game.py

from wall import Wall
from window import Window
from player import Player
from time import clock
__author__ = 'Seth Tinglof'
__version__ = '1.0'


class Game:

    SIZE_X = 1280
    SIZE_Y = 720

    def __init__(self):
        """
        Starts a new Tron game
        :return: self
        """
        self.walls = []
        self.characters = []
        self.playing = True
        self.blue_score = 0
        self.red_score = 0
        self.frame = 0
        self.create_characters()
        self.create_initial_walls()
        self.wall_start = [[100, 350], [1180, 350]]
        self.window = Window(self.characters, self.walls)
        self.window.root.after(10, self.intro)
        self.window.root.mainloop()

    def create_characters(self):
        """
        Creates the players characters
        :return: None
        """
        self.characters.append(Player(100, 350, 'blue', 0))
        self.characters.append(Player(1180, 350, 'red', 180))

    def create_initial_walls(self):
        """
        Creates walls around the border of the map.
        :return: None
        """
        self.walls.append(Wall(True, 0, 1280, 0, 'black'))
        self.walls.append(Wall(True, 0, 1280, 707, 'black'))
        self.walls.append(Wall(False, 0, 0, 720, 'black'))
        self.walls.append(Wall(False, 1280, 0, 720, 'black'))

    def create_wall(self, player_number):
        """
        Creates a new wall that the players cannot cross based on the last position that the player turned and
        the players current position.
        :param player_number: The index of the player who the wall is being created from.
        :return: a new Wall object.
        """
        horizontal = self.wall_start[player_number][1] == self.characters[player_number].get_y_pos()
        if horizontal:
            if self.wall_start[player_number][0] < self.characters[player_number].get_x_pos():
                new_wall = Wall(horizontal, self.wall_start[player_number][0], self.characters[player_number].get_x_pos(),
                                self.characters[player_number].get_y_pos(), self.characters[player_number].get_color())
            else:
                new_wall = Wall(horizontal, self.characters[player_number].get_x_pos(), self.wall_start[player_number][0],
                                self.characters[player_number].get_y_pos(), self.characters[player_number].get_color())
        else:
            if self.wall_start[player_number][1] < self.characters[player_number].get_y_pos():
                new_wall = Wall(horizontal, self.wall_start[player_number][0], self.wall_start[player_number][1],
                                self.characters[player_number].get_y_pos(), self.characters[player_number].get_color())
            else:
                new_wall = Wall(horizontal, self.wall_start[player_number][0], self.characters[player_number].get_y_pos(),
                                self.wall_start[player_number][1], self.characters[player_number].get_color())
        return new_wall

    def add_wall(self, player_num):
        """
        Adds a wall to the list of wall that the player has drawn.  This wall lasts the duration of the game,
        This method is meant only to be used when the player turns.
        :param player_num: Index of player that is getting the new wall.
        :return: None
        """
        wall = self.create_wall(player_num)
        self.walls.append(wall)
        self.characters[player_num].unhittable_walls[1] = wall
        self.wall_start[player_num] = [self.characters[player_num].get_x_pos(), self.characters[player_num].get_y_pos()]

    def create_temp_walls(self):
        """
        Creates temporary walls that only last for this frame.  These are the walls actively created behind the player.
        :return: None
        """
        temp_walls = []
        for i in range(len(self.characters)):
            temp_walls.append(self.create_wall(i))
            self.walls.append(temp_walls[i])
            self.characters[i].unhittable_walls[0] = temp_walls[i]
        return temp_walls

    def delete_temp_walls(self, temp_walls):
        """
        Removes temporary walls at the end of the frame.
        :param temp_walls: wall objects to be removed in a list.
        :return: None
        """
        for wall in temp_walls:
            self.walls.remove(wall)

    def collisions_check(self):
        """
        Checks if either player has hit a wall.  If one player has, then the other wins.
        :return: None
        """
        for wall in self.walls:
            for i in range(len(self.characters)):
                if wall.check_collision(self.characters[i]) and not wall == self.characters[i].unhittable_walls[0]\
                        and not wall == self.characters[i].unhittable_walls[1]:
                    self.playing = False
                    if i == 0:
                        self.red_score += 1
                    else:
                        self.blue_score += 1
                    self.window.set_score(self.blue_score, self.red_score)

    def intro(self):
        self.window.intro()
        self.window.play_button['command'] = self.start_game

    def start_game(self):
        """
        Begins playing game for the first time.
        :return: None
        """
        self.window.intro_frame.pack_forget()
        self.window.center_frame.pack()
        self.window.root.bind("<KeyPress>", self.key_pressed)
        self.game_loop()

    def game_loop(self):
        """
        Main game loop.  Runs for the duration of the game.
        :return: None
        """
        while True:
            next_time = 0
            while self.playing:
                current_time = clock()
                if current_time >= next_time:
                    for character in self.characters:
                        character.move()
                    temp_walls = self.create_temp_walls()
                    self.window.update_canvas()
                    self.collisions_check()
                    self.delete_temp_walls(temp_walls)
                    next_time = current_time + 1 / 60
                    self.frame += 1
            self.walls = []
            self.characters = []
            self.window.walls = self.walls
            self.window.characters = self.characters
            self.playing = True
            self.create_characters()
            self.create_initial_walls()
            self.wall_start = [[100, 350], [1180, 350]]

    def key_pressed(self, event):
        """
        Responds to key pressed events.  Allows users to control their characters.
        :param event: Key pressed event.
        :return: None
        """
        ######################
        # Player One
        ######################
        if event.char == 'a' and not self.characters[0].get_angle() == 0 \
                and not self.characters[0].get_angle() == 180 and self.characters[0].last_turn_frame <= self.frame - 2:
            self.characters[0].set_angle(180)
            self.add_wall(0)
            self.characters[0].last_turn_frame = self.frame
        elif event.char == 'w' and not self.characters[0].get_angle() == 270 \
                and not self.characters[0].get_angle() == 90 and self.characters[0].last_turn_frame <= self.frame - 2:
            self.characters[0].set_angle(90)
            self.add_wall(0)
            self.characters[0].last_turn_frame = self.frame
        elif event.char == 'd' and not self.characters[0].get_angle() == 180 \
                and not self.characters[0].get_angle() == 0 and self.characters[0].last_turn_frame <= self.frame - 2:
            self.characters[0].set_angle(0)
            self.add_wall(0)
            self.characters[0].last_turn_frame = self.frame
        elif event.char == 's' and not self.characters[0].get_angle() == 90 \
                and not self.characters[0].get_angle() == 270 and self.characters[0].last_turn_frame <= self.frame - 2:
            self.characters[0].set_angle(270)
            self.add_wall(0)
            self.characters[0].last_turn_frame = self.frame
        ######################
        # Player Two
        ######################
        elif event.keysym == 'Left' and not self.characters[1].get_angle() == 0 \
                and not self.characters[1].get_angle() == 180 and self.characters[1].last_turn_frame <= self.frame - 2:
            self.characters[1].set_angle(180)
            self.add_wall(1)
            self.characters[1].last_turn_frame = self.frame
        elif event.keysym == 'Up' and not self.characters[1].get_angle() == 270 \
                and not self.characters[1].get_angle() == 90 and self.characters[1].last_turn_frame <= self.frame - 2:
            self.characters[1].set_angle(90)
            self.add_wall(1)
            self.characters[1].last_turn_frame = self.frame
        elif event.keysym == 'Right' and not self.characters[1].get_angle() == 180 \
                and not self.characters[1].get_angle() == 0 and self.characters[1].last_turn_frame <= self.frame - 2:
            self.characters[1].set_angle(0)
            self.add_wall(1)
            self.characters[1].last_turn_frame = self.frame
        elif event.keysym == 'Down' and not self.characters[1].get_angle() == 90 \
                and not self.characters[1].get_angle() == 270 and self.characters[1].last_turn_frame <= self.frame - 2:
            self.characters[1].set_angle(270)
            self.add_wall(1)
            print(self.characters[1].last_turn_frame)
            print(self.frame)
            self.characters[1].last_turn_frame = self.frame
