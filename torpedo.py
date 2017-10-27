
# Some essential constants
INITIAL_TORPEDO_X_VELOCITY = 0
INITIAL_TORPEDO_Y_VELOCITY = 0
TORPEDO_RADIUS = 4
LIVES = 200

class Torpedo:

    def __init__(self, ship):

        self.__x_position = ship.get_x_position()
        self.__y_position = ship.get_y_position()
        self.__direction = ship.get_direction()
        self.__x_velocity = INITIAL_TORPEDO_X_VELOCITY
        self.__y_velocity = INITIAL_TORPEDO_Y_VELOCITY
        self.__life = LIVES
        self.__fire_status = False  # becomes true if the torpedo was fires

    # Some getters and setters
    def get_x_position(self):
        return float(self.__x_position)

    def get_y_position(self):
        return float(self.__y_position)

    def get_direction(self):
        return float(self.__direction)

    def get_x_velocity(self):
        return float(self.__x_velocity)

    def get_y_velocity(self):
        return float(self.__y_velocity)

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

    def get_life(self):
        return self.__life

    def set_life(self, life):
        self.__life = life

    def get_fire_status(self):
        return self.__fire_status

    def set_fire_status(self, fire_status):
        self.__fire_status = fire_status

    def get_radius(self):
        return TORPEDO_RADIUS

