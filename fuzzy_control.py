from fuzz import TrapezoidalFuzzyNumber as Trapezoid


class FuzzyControl:
    def __init__(self):
        self.height_sets = {'low': Trapezoid((0, 13), (0, 50)),
                            'medium': Trapezoid((50, 63), (35, 75)),
                            'high': Trapezoid((75, 100), (55, 100))}

        self.y_velocity_sets = {'safe': Trapezoid((0, 3), (0, 5)),
                                'medium': Trapezoid((5, 60), (4, 90)),
                                'fast': Trapezoid((90, 310), (50, 310))}

        self.position_sets = {'left': Trapezoid((-5, -0.3), (-5, -0.2)),
                              'safe': Trapezoid((-0.1, 0.1), (-0.3, 0.3)),
                              'right': Trapezoid((0.3, 5), (0.2, 5))}

        self.x_velocity_sets = {'left': Trapezoid((-5, -2), (-5, -1)),
                                'slow': Trapezoid((-0.5, 0.5), (-2, 2)),
                                'right': Trapezoid((2, 5), (1, 5))}

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
                   rules[3]*2, rules[4]*1, rules[5]*0,
                   rules[6]*3, rules[7]*2, rules[8]*0))/sum(rules)
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

        thrust = sum((rules[0]*0.3, rules[1]*0.2, rules[2]*0.1,
                      rules[3]*0.1, rules[4]*0, rules[5]*-0.1,
                      rules[6]*-0.3, rules[7]*-0.2, rules[8]*-0.1))/sum(rules)
        return thrust

    def control_input(self, height, y_velocity, position, x_velocity):
        burn = self._get_burn(height, y_velocity)
        thrust = self._get_thrust(height, y_velocity)
        return burn, thrust
