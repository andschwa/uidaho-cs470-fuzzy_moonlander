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

        self.position_sets = {'negative': Trapezoid((-MAX, -0.7), (-MAX, -0.2)),
                              'zero': Trapezoid((-0.1, 0.1), (-0.2, 0.2)),
                              'positive': Trapezoid((0.7, MAX), (0.2, MAX))}

        self.x_velocity_sets = {'left': Trapezoid((-MAX, -0.6), (-MAX, -0.2)),
                                'middle': Trapezoid((-0.2, 0.2), (-0.3, 0.3)),
                                'right': Trapezoid((0.6, MAX), (0.2, MAX))}

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
                   rules[6]*9, rules[7]*5, rules[8]*0))/sum(rules)
        return burn

    def _get_thrust(self, position, velocity):
        rules = []
        print(position, velocity)
        rules.append(min(self.position_sets['negative'].mu(position),
                         self.x_velocity_sets['left'].mu(velocity)))
        rules.append(min(self.position_sets['negative'].mu(position),
                         self.x_velocity_sets['middle'].mu(velocity)))
        rules.append(min(self.position_sets['negative'].mu(position),
                         self.x_velocity_sets['right'].mu(velocity)))

        rules.append(min(self.position_sets['zero'].mu(position),
                         self.x_velocity_sets['left'].mu(velocity)))
        rules.append(min(self.position_sets['zero'].mu(position),
                         self.x_velocity_sets['middle'].mu(velocity)))
        rules.append(min(self.position_sets['zero'].mu(position),
                         self.x_velocity_sets['right'].mu(velocity)))

        rules.append(min(self.position_sets['positive'].mu(position),
                         self.x_velocity_sets['left'].mu(velocity)))
        rules.append(min(self.position_sets['positive'].mu(position),
                         self.x_velocity_sets['middle'].mu(velocity)))
        rules.append(min(self.position_sets['positive'].mu(position),
                         self.x_velocity_sets['right'].mu(velocity)))
        print(rules)

        thrust = sum((rules[0]*-2.5, rules[1]*-1.9, rules[2]*0.0,
                      rules[3]*-0.0, rules[4]*0.0, rules[5]*0.0,
                      rules[6]*0.0, rules[7]*1.9, rules[8]*2.5))/sum(rules)
        return thrust

    def control_input(self, height, y_velocity, position, x_velocity, wind):
        burn = self._get_burn(height, y_velocity)
        thrust = self._get_thrust(10*position, 10*x_velocity)/10
        return burn, thrust
