import random
from screen import Screen

# Some essential constants
HORIZONTAL = 0
INITIAL_X = random.randrange(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
INITIAL_Y = random.randrange(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
INITIAL_VELOCITY_X = 0
INITIAL_VELOCITY_Y = 0
RADIUS = 1
LIVES = 3


class Ship:

    def __init__(self):
        self.__x_position = INITIAL_X
        self.__y_position = INITIAL_Y
        self.__x_velocity = INITIAL_VELOCITY_X
        self.__y_velocity = INITIAL_VELOCITY_Y
        self.__direction = HORIZONTAL  # in degrees clockwise
        self.__lives = LIVES

    # Some getters and setters
    def get_x_position(self):
        return float(self.__x_position)

    def get_y_position(self):
        return float(self.__y_position)

    def get_x_velocity(self):
        return float(self.__x_velocity)

    def get_y_velocity(self):
        return float(self.__y_velocity)

    def get_direction(self):
        return float(self.__direction)

    def get_lives(self):
        return self.__lives

    def set_direction(self, direction):
        self.__direction = direction

    def set_x_position(self, x_position):
        self.__x_position = x_position

    def set_y_position(self, y_position):
        self.__y_position = y_position

    def set_x_velocity(self, x_velocity):
        self.__x_velocity = x_velocity

    def set_y_velocity(self, y_velocity):
        self.__y_velocity = y_velocity

    def set_lives(self, lives):
        self.__lives = lives

    def get_radius(self):
        return RADIUS
