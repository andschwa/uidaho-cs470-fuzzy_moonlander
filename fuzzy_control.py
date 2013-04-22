import sys
from fuzz import TrapezoidalFuzzyNumber as Trapezoid


class FuzzyControl:
    def __init__(self):
        MAX = float(sys.maxint)
        self.height_sets = {'low': Trapezoid((-MAX, 20.0), (-MAX, 40.0)),
                            'medium': Trapezoid((50.0, 50.0), (30.0, 70.0)),
                            'high': Trapezoid((70.0, MAX), (60.0, MAX))}

        self.y_velocity_sets = {'safe': Trapezoid((-MAX, 3.0), (-MAX, 4.0)),
                                'medium': Trapezoid((5.0, 20.0), (3.5, 40.0)),
                                'fast': Trapezoid((50.0, MAX), (35.0, MAX))}

        self.position_sets = {'low': Trapezoid((-MAX, 1.6), (-MAX, 2.0)),
                              'medium': Trapezoid((2.4, 2.4), (1.8, 3.0)),
                              'high': Trapezoid((3.6, MAX), (3.0, MAX))}

        self.x_velocity_sets = {'safe': Trapezoid((-MAX, 0.3), (-MAX, 0.5)),
                                'medium': Trapezoid((0.5, 0.5), (0.3, 0.7)),
                                'fast': Trapezoid((0.7, MAX), (0.5, MAX))}
        self.wind_direction = None

    def _get_burn(self, position, velocity):
        rules = []
        rules.append(min(self.height_sets['high'].mu(position),
                         self.y_velocity_sets['fast'].mu(velocity)))
        rules.append(min(self.height_sets['high'].mu(position),
                         self.y_velocity_sets['medium'].mu(velocity)))
        rules.append(min(self.height_sets['high'].mu(position),
                         self.y_velocity_sets['safe'].mu(velocity)))

        rules.append(min(self.height_sets['medium'].mu(position),
                         self.y_velocity_sets['fast'].mu(velocity)))
        rules.append(min(self.height_sets['medium'].mu(position),
                         self.y_velocity_sets['medium'].mu(velocity)))
        rules.append(min(self.height_sets['medium'].mu(position),
                         self.y_velocity_sets['safe'].mu(velocity)))

        rules.append(min(self.height_sets['low'].mu(position),
                         self.y_velocity_sets['fast'].mu(velocity)))
        rules.append(min(self.height_sets['low'].mu(position),
                         self.y_velocity_sets['medium'].mu(velocity)))
        rules.append(min(self.height_sets['low'].mu(position),
                         self.y_velocity_sets['safe'].mu(velocity)))

        burn = sum((rules[0]*1, rules[1]*0, rules[2]*0,
                   rules[3]*6, rules[4]*4, rules[5]*0,
                   rules[6]*12, rules[7]*8, rules[8]*1))/sum(rules)
        return burn

    def _get_thrust(self, position, velocity):
        rules = []
        rules.append(min(self.position_sets['high'].mu(position),
                         self.x_velocity_sets['fast'].mu(velocity)))
        rules.append(min(self.position_sets['high'].mu(position),
                         self.x_velocity_sets['medium'].mu(velocity)))
        rules.append(min(self.position_sets['high'].mu(position),
                         self.x_velocity_sets['safe'].mu(velocity)))

        rules.append(min(self.position_sets['medium'].mu(position),
                         self.x_velocity_sets['fast'].mu(velocity)))
        rules.append(min(self.position_sets['medium'].mu(position),
                         self.x_velocity_sets['medium'].mu(velocity)))
        rules.append(min(self.position_sets['medium'].mu(position),
                         self.x_velocity_sets['safe'].mu(velocity)))

        rules.append(min(self.position_sets['low'].mu(position),
                         self.x_velocity_sets['fast'].mu(velocity)))
        rules.append(min(self.position_sets['low'].mu(position),
                         self.x_velocity_sets['medium'].mu(velocity)))
        rules.append(min(self.position_sets['low'].mu(position),
                         self.x_velocity_sets['safe'].mu(velocity)))

        thrust = sum((rules[0]*1.0, rules[1]*0.7, rules[2]*0.3,
                      rules[3]*0.7, rules[4]*0.4, rules[5]*0.3,
                      rules[6]*0.3, rules[7]*0.1, rules[8]*0.0))/sum(rules)
        return -self.wind_direction * thrust

    def control_input(self, height, y_velocity, position, x_velocity):
        burn = self._get_burn(height, y_velocity)
        if self.wind_direction is None:
            self.wind_direction = x_velocity/x_velocity
        thrust = self._get_thrust(10*position, 10*x_velocity)
        return burn, thrust
