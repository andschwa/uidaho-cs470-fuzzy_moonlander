import sys
from fuzz import TrapezoidalFuzzyNumber as Trapezoid


class FuzzyControl:
    def __init__(self):
        MAX = float(sys.maxint)
        self.height_sets = {'low': Trapezoid((-MAX, 20.0), (-MAX, 40.0)),
                            'medium': Trapezoid((50.0, 50.0), (30.0, 70.0)),
                            'high': Trapezoid((70.0, MAX), (60.0, MAX))}

        self.y_velocity_sets = {'safe': Trapezoid((-MAX, 3.0), (-MAX, 4.0)),
                                'medium': Trapezoid((9.0, 15.0), (4.0, 30.0)),
                                'fast': Trapezoid((35.0, MAX), (25.0, MAX))}

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
                   rules[3]*8, rules[4]*4, rules[5]*0,
                   rules[6]*14, rules[7]*6, rules[8]*1))/sum(rules)
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

        thrust = sum((rules[0]*2.0, rules[1]*1.7, rules[2]*1.0,
                      rules[3]*1.2, rules[4]*0.9, rules[5]*0.6,
                      rules[6]*0.8, rules[7]*0.5, rules[8]*0.1))/sum(rules)
        return self.wind_direction * thrust

    def control_input(self, height, y_velocity, position, x_velocity, wind):
        burn = self._get_burn(height, y_velocity)
        if self.wind_direction is None:
            self.wind_direction = wind/wind
        thrust = self._get_thrust(10*abs(position), 10*abs(x_velocity))
        return burn, 0
