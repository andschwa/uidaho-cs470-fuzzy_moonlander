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

        self.position_sets = {'left': Trapezoid((-MAX, -0.3), (-MAX, -0.2)),
                              'safe': Trapezoid((-0.2, 0.2), (-0.25, 0.25)),
                              'right': Trapezoid((0.3, MAX), (0.2, MAX))}

        self.x_velocity_sets = {'left': Trapezoid((-MAX, -0.4), (-MAX, -0.2)),
                                'slow': Trapezoid((-0.08, 0.08), (-0.2, 0.2)),
                                'right': Trapezoid((0.4, MAX), (0.2, MAX))}

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
                   rules[6]*9, rules[7]*7, rules[8]*0.5))/sum(rules)
        return burn

    def _get_thrust(self, position, velocity):
        rules = []
        rules.append(min(self.position_sets['left'].mu(position),
                         self.x_velocity_sets['left'].mu(velocity)))
        rules.append(min(self.position_sets['left'].mu(position),
                         self.x_velocity_sets['slow'].mu(velocity)))
        rules.append(min(self.position_sets['left'].mu(position),
                         self.x_velocity_sets['right'].mu(velocity)))

        rules.append(min(self.position_sets['safe'].mu(position),
                         self.x_velocity_sets['left'].mu(velocity)))
        rules.append(min(self.position_sets['safe'].mu(position),
                         self.x_velocity_sets['slow'].mu(velocity)))
        rules.append(min(self.position_sets['safe'].mu(position),
                         self.x_velocity_sets['right'].mu(velocity)))

        rules.append(min(self.position_sets['right'].mu(position),
                         self.x_velocity_sets['left'].mu(velocity)))
        rules.append(min(self.position_sets['right'].mu(position),
                         self.x_velocity_sets['slow'].mu(velocity)))
        rules.append(min(self.position_sets['right'].mu(position),
                         self.x_velocity_sets['right'].mu(velocity)))

        thrust = sum((rules[0]*0.1, rules[1]*0.02, rules[2]*0,
                      rules[3]*0.1, rules[4]*0, rules[5]*-0.1,
                      rules[6]*0, rules[7]*-0.02, rules[8]*-0.1))/sum(rules)
        return thrust

    def control_input(self, height, y_velocity, position, x_velocity):
        burn = self._get_burn(height, y_velocity)
        thrust = self._get_thrust(height, y_velocity)
        return burn, thrust
