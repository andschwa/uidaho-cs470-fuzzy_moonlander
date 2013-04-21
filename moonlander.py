import random


class Moonlander:
    def __init__(self):
        self.acceleration = random.randint(10, 30)/10  # 1-3 by 0.1
        self.wind = 0.2 * random.random()

        self.max_safe_landing_speed = 4.0
        self.min_safe_x = -0.2
        self.max_safe_x = 0.2

        self.landed = 'in_air'
        self.height = 100.0
        self.x_position = 0
        self.y_velocity = 10.0 * random.random()
        self.x_velocity = 0
        self.fuel = 100.0
        self.burn = None
        self.thrust = None

    def control(self):
        """
        This needs to get burn and thrust from the ANN
        """
        self.burn = 1.0
        self.thrust = 0

    def test(self):
        if self.height > 0:
            return 'in_air'
        if (self.y_velocity > self.max_safe_landing_speed or
                self.x_position < self.min_safe_x or
                self.x_position > self.max_safe_x):
            return 'crashed'
        else:
            return 'landed'

    def update(self):
        self.y_velocity += self.acceleration
        self.control()

        if self.fuel < self.burn:
            self.burn = self.fuel
        self.fuel -= abs(self.burn)
        self.y_velocity -= self.burn

        if self.fuel < self.thrust:
            self.thrust = self.fuel
        self.fuel -= abs(self.thrust)
        self.x_velocity -= self.thrust

        self.height -= self.y_velocity
        self.x_position += self.x_velocity + self.wind

    def output(self):
        output = {'Height': self.height,
                  'Y-Velocity': self.y_velocity,
                  'Position': self.x_position,
                  'X-Velocity': self.x_position,
                  'Fuel': self.fuel}
        for string, variable in output.items():
            print(string+': {}'.format(variable))
