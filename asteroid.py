import random
from screen import Screen
import ship
import math

# Some essential constants
INITIAL_X = random.randrange(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
INITIAL_Y = random.randrange(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
MIN_VELOCITY = 3
MAX_VELOCITY = 10
INITIAL_VELOCITY_X = random.randrange(MIN_VELOCITY, MAX_VELOCITY)
INITIAL_VELOCITY_Y = random.randrange(MIN_VELOCITY, MAX_VELOCITY)
DEFAULT_SIZE = 3
SQUARE = 2
ASTEROID_RADIUS_SIZE = 10
ASTEROID_RADIUS_NORMAL = 5


class Asteroid:

    def __init__(self):

        while True:  # making sure that each asteroid won't land on ship location
            self.__x_position = random.randrange(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
            self.__y_position = random.randrange(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
            if ship.INITIAL_X != self.__x_position and \
               ship.INITIAL_Y != self.__y_position:
                break
        self.__x_velocity = INITIAL_VELOCITY_X
        self.__y_velocity = INITIAL_VELOCITY_Y
        self.__size = DEFAULT_SIZE

    # Some getters and setters
    def get_x_position(self):
        return self.__x_position

    def get_y_position(self):
        return self.__y_position

    def get_x_velocity(self):
        return self.__x_velocity

    def get_y_velocity(self):
        return self.__y_velocity

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def set_x_position(self, x_position):
        self.__x_position = x_position

    def set_y_position(self, y_position):
        self.__y_position = y_position

    def set_x_velocity(self, x_velocity):
        self.__x_velocity = x_velocity

    def set_y_velocity(self, y_velocity):
        self.__y_velocity = y_velocity

    def get_radius(self):
        """
        :return: The radius of the of the asteroid
        """
        return self.get_size() * ASTEROID_RADIUS_SIZE - \
               ASTEROID_RADIUS_NORMAL

    def has_intersection(self, obj):
        """
        :param obj: either a torpedo or the ship
        :return: True, if the given object is
        intersected with the asteroid, False, otherwise
        """
        distance_x = math.pow(obj.get_x_position() - self.get_x_position(), SQUARE)
        distance_y = math.pow(obj.get_y_position() - self.get_y_position(), SQUARE)
        distance = math.sqrt(distance_x + distance_y)

        return distance <= self.get_radius() + self.get_radius()
