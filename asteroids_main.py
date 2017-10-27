from screen import Screen
import sys
import math
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

# Some essential constants
DEFAULT_ASTEROIDS_NUM = 5
LEFT_ROTATION_ANGLE = 6
RIGHT_ROTATION_ANGLE = -6
HIT_TITLE = "You're hit!"
HIT_MESSAGE = "Watch Out!"
GAME_OVER_TITLE = "Game Over"
GAME_OVER_MESSAGE = "See you later..."
WIN_TITLE = "Congratulations!"
WIN_MESSAGE = "You Won!"
ACCELERATION_FACTOR = 2
TORPEDO_AMNT = 15
TORPEDO_INIT_LIVES = 200
TORPEDO_LIFE = 1
TORPEDO_INIT_VELOCITY = 0
LARGE_ASTEROID = 3
MEDIUM_ASTEROID = 2
SMALL_ASTEROID = 1
LARGE_SCORE = 20
MEDIUM_SCORE = 50
SMALL_SCORE = 100
SQUARE = 2
SHIP_LIFE = 1
COLLISION_CONSTANT = -1


class GameRunner:

    def __init__(self, asteroids_amnt):
        self._screen = Screen()
        self._ship = Ship()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self._asteroids = list()
        self._torpedoes = list()
        for i in range(asteroids_amnt):
            asteroid = Asteroid()
            self._screen.register_asteroid(asteroid,
                                           asteroid.get_size())
            self._asteroids.append(asteroid)

        for i in range(TORPEDO_AMNT):
            self._torpedoes.append(Torpedo(self._ship))

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop,5)

    def _game_loop(self):
        '''
         The main loop of the game
        '''
        self._screen.draw_ship(self._ship.get_x_position(),
                               self._ship.get_y_position(),
                               self._ship.get_direction())
        self._draw_asteroids()
        self._accelerate(self._ship)
        self._rotate(self._ship)
        self._update_position(self._ship)
        self._ship_collision()
        self._fire()
        self._update_torpedo_position()
        self._move_asteroids()
        self._quit_game()

    def _draw_asteroids(self):
        """
        :return: The function draw all asteroids to the screen
        """
        for asteroid in self._asteroids:
            self._screen.draw_asteroid(asteroid,
                                       asteroid.get_x_position(),
                                       asteroid.get_y_position())

    def _move_asteroids(self):
        """
        :return: the function moves all asteroids on the screen
        """
        for asteroid in self._asteroids:
            self._update_position(asteroid)

    def _update_position(self, obj):
        """
        :param obj: a Ship, Asteroid, or Torpedo object
        :return: the function calculates the position of the object
        by using the transition formula, and updates the position of the object
        accordingly
        """

        delta_x = self.screen_max_x - self.screen_min_x
        delta_y = self.screen_max_y - self.screen_min_y

        new_coords_x = ((obj.get_x_velocity() + (obj.get_x_position() -
                        self.screen_min_x)) % delta_x) + self.screen_min_x
        new_coords_y = ((obj.get_y_velocity() + (obj.get_y_position() -
                        self.screen_min_y)) % delta_y) + self.screen_min_y

        obj.set_x_position(new_coords_x)
        obj.set_y_position(new_coords_y)

    def _update_torpedo_position(self):
        """
        :return: The function updates the position of the torpedos
         in the following way:
         if the torpedo was not fired, the function updates the position
         to the current position of the ship.
         otherwise, the function update the position of torpedo
         according to the formula
         In addition, the function determines if a torpedo
         hit an asteroid, and updates the life of the torpedo.
        """
        for torpedo in self._torpedoes:
            if not torpedo.get_fire_status():
                torpedo.set_x_position(self._ship.get_x_position())
                torpedo.set_y_position(self._ship.get_y_position())
                torpedo.set_direction(self._ship.get_direction())
                torpedo.set_x_velocity(self._ship.get_x_velocity())
                torpedo.set_y_velocity(self._ship.get_y_velocity())
            else:
                self._update_position(torpedo)
                self._screen.draw_torpedo(torpedo,
                                          torpedo.get_x_position(),
                                          torpedo.get_y_position(),
                                          torpedo.get_direction())
                self._torpedo_collision(torpedo)
                torpedo.set_life(torpedo.get_life() -
                                 TORPEDO_LIFE)
                self._check_life(torpedo)

    def _rotate(self, ship):
        """
        :param ship: Ship object
        :return: The function rotates the ship according to player's choice,
         left of right
        """
        if self._screen.is_left_pressed():
            ship.set_direction(ship.get_direction() + LEFT_ROTATION_ANGLE)
        if self._screen.is_right_pressed():
            ship.set_direction(ship.get_direction() + RIGHT_ROTATION_ANGLE)

    def _accelerate(self, ship):
        """
        :param ship: a Ship object
        :return: if the up arrow key is pressed the function accelerates
         the ship, and updates the position
        """

        if self._screen.is_up_pressed():
            velocity_x = ship.get_x_velocity() + math.cos(math.radians(ship.get_direction()))
            velocity_y = ship.get_y_velocity() + math.sin(math.radians(ship.get_direction()))
            ship.set_x_velocity(velocity_x)
            ship.set_y_velocity(velocity_y)


    def _ship_collision(self):
        """
        :return: the function determines if the ship hit an asteroid,
        if it did, the relevant message is shown to the screen,
        and one life is removed from the ship
        """

        for asteroid in self._asteroids:
            if asteroid.has_intersection(self._ship):
                self._screen.show_message(HIT_TITLE, HIT_MESSAGE)
                self._screen.remove_life()
                self._screen.unregister_asteroid(asteroid)
                self._asteroids.remove(asteroid)
                self._ship.set_lives(self._ship.get_lives() - SHIP_LIFE)

    def _torpedo_collision(self, torpedo):
        """
        :param torpedo: Torpedo object
        :return: The function determines if the given torpedo hit
        an asteroid, if it did, the asteroid is split,
        and the score is updated accordingly,
        """
        for asteroid in self._asteroids:
                if asteroid.has_intersection(torpedo):
                    if asteroid.get_size() == LARGE_ASTEROID:
                        self._screen.set_score(LARGE_SCORE)
                    elif asteroid.get_size() == MEDIUM_ASTEROID:
                        self._screen.set_score(MEDIUM_SCORE)
                    elif asteroid.get_size() == SMALL_ASTEROID:
                        self._screen.set_score(SMALL_SCORE)
                    self._split_asteroid(asteroid, torpedo)

    def _fire(self):
        """
        :return: if the up arrow key is pressed the function fires
        a torpedo from the ship, by calculating and updating torpedo's
        velocity and drawing torpedo to the screen
        """

        if self._screen.is_space_pressed():

            for torpedo in self._torpedoes:
                if not torpedo.get_fire_status():  # if the torpedo hasn't been fired yet
                    torpedo.set_fire_status(not torpedo.get_fire_status())
                    self._screen.register_torpedo(torpedo)

                    new_velocity_x = torpedo.get_x_velocity() + \
                    ACCELERATION_FACTOR * math.cos(math.radians(torpedo.get_direction()))

                    new_velocity_y = torpedo.get_y_velocity() + \
                    ACCELERATION_FACTOR * math.sin(math.radians(torpedo.get_direction()))

                    torpedo.set_x_velocity(new_velocity_x)
                    torpedo.set_y_velocity(new_velocity_y)

                    self._screen.draw_torpedo(torpedo,
                                              torpedo.get_x_position(),
                                              torpedo.get_y_position(),
                                              torpedo.get_direction())
                    break

    def _check_life(self, torpedo):
        """
        :param torpedo: Torpedo object
        :return: if the given torpedo has run out of lives, the function
        removes the torpedo from the screen, updates its fire status and
        rewrites its lives
        """

        if not torpedo.get_life():  # is zero
            self._screen.unregister_torpedo(torpedo)
            torpedo.set_x_velocity(TORPEDO_INIT_VELOCITY)
            torpedo.set_y_velocity(TORPEDO_INIT_VELOCITY)
            torpedo.set_life(TORPEDO_INIT_LIVES)
            torpedo.set_fire_status(not torpedo.get_fire_status())

    def _split_asteroid(self, asteroid, torpedo):
        """
        :param asteroid: Asteroid object
        :param torpedo: Torpedo object
        :return: the function splits the asteroid, according
        to its size by creating 2 fractures and removing the
        original asteroid from the screen
        """

        if asteroid.get_size() == LARGE_ASTEROID:
            self._create_fractures(asteroid, torpedo, MEDIUM_ASTEROID)
        elif asteroid.get_size() == MEDIUM_ASTEROID:
            self._create_fractures(asteroid, torpedo, SMALL_ASTEROID)
        else:  # SMALL_ASTEROID
            self._asteroids.remove(asteroid)
            self._screen.unregister_asteroid(asteroid)

    def _create_fractures(self, asteroid, torpedo, asteroid_size):
        """
        :param asteroid: an Asteroid object
        :param torpedo: a Torpedo object
        :param asteroid_size: the size of the asteroid
        :return: The function splits the given asteroid by
        creating 2 smaller asteroids, drawing them
        to the screen. The velocity of the smaller asteroids
        is calculated according to the formula.
        """
        fracture1 = Asteroid()
        fracture1.set_size(asteroid_size)
        fracture2 = Asteroid()
        fracture2.set_size(asteroid_size)
        fracture1.set_x_position(asteroid.get_x_position())
        fracture1.set_y_position(asteroid.get_y_position())
        fracture2.set_x_position(asteroid.get_x_position())
        fracture2.set_y_position(asteroid.get_y_position())
        self._set_collision_velocity(asteroid, torpedo, fracture1)
        self._set_collision_velocity(asteroid, torpedo, fracture2)
        fracture2.set_x_velocity(COLLISION_CONSTANT * fracture2.get_x_velocity())
        fracture2.set_y_velocity(COLLISION_CONSTANT * fracture2.get_y_velocity())
        self._screen.unregister_asteroid(asteroid)
        self._asteroids.remove(asteroid)
        self._asteroids.append(fracture1)
        self._asteroids.append(fracture2)
        self._screen.register_asteroid(fracture1, fracture1.get_size())
        self._screen.register_asteroid(fracture2, fracture2.get_size())

    def _set_collision_velocity(self, asteroid, torpedo, fracture):
        """
        :param asteroid: an Asteroid object
        :param torpedo: a Torpedo object
        :param fracture: an Asteroid object
        :return: The function sets the velocity of the fracture
        according to the formula
        """

        delta = math.sqrt((math.pow(asteroid.get_x_velocity(), SQUARE)) +
                          (math.pow(asteroid.get_y_velocity(), SQUARE)))
        new_x_velocity = (torpedo.get_x_velocity() + asteroid.get_x_velocity()) / delta
        new_y_velocity = (torpedo.get_y_velocity() + asteroid.get_y_velocity()) / delta
        fracture.set_x_velocity(new_x_velocity)
        fracture.set_y_velocity(new_y_velocity)

    def _quit_game(self):
        """
        :return: the function ends the game if the player pressed "q"
        of if the ship has run out of lives of if all asteroid were destroyed
        """
        if self._screen.should_end():  # pressed "q"
            self._screen.end_game()
            self._screen.show_message(GAME_OVER_TITLE, GAME_OVER_MESSAGE)
            sys.exit()
        elif not self._ship.get_lives():  # zero lives
            self._screen.end_game()
            self._screen.show_message(GAME_OVER_TITLE, GAME_OVER_MESSAGE)
            sys.exit()
        elif not len(self._asteroids):  # zero asteroids
            self._screen.end_game()
            self._screen.show_message(WIN_TITLE, WIN_MESSAGE)
            sys.exit()


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )
