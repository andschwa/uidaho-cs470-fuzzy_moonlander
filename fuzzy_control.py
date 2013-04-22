from fuzz import TrapezoidalFuzzyNumber as Trapezoid


class FuzzyControl:
    def __init__(self):
        self.vertical_sets = ['low', 'medium', 'high']
        self.height_sets = [Trapezoid((0, 13), (0, 50)),
                            Trapezoid((50, 63), (35, 75)),
                            Trapezoid((75, 100), (55, 100))]

        self.y_velocity_sets = [Trapezoid((0, 3), (0, 5)),
                                Trapezoid((5, 60), (4, 90)),
                                Trapezoid((90, 310), (50, 310))]

        self.horizontal_sets = ['left', 'safe', 'right']
        self.position_sets = [Trapezoid((-5, -0.3), (-5, -0.2)),
                              Trapezoid((-0.1, 0.1), (-0.3, 0.3)),
                              Trapezoid((0.3, 5), (0.2, 5))]

        self.x_velocity_sets = [Trapezoid((-5, -2), (-5, -1)),
                                Trapezoid((-0.5, 0.5), (-2, 2)),
                                Trapezoid((2, 5), (1, 5))]
        self.sets = [self.height_sets,
                     self.y_velocity_sets,
                     self.position_sets,
                     self.x_velocity_sets]

    def control_input(self, height, y_velocity, position, x_velocity):
        burn, thrust = 0, 0
        inputs = [height, y_velocity, position, x_velocity]
        for i in range(len(inputs)):
            sets = self.sets[i]
            print('Input #{}'.format(i))
            for j in range(len(sets)):
                print(str(inputs[i]) +
                      ': ' +
                      self.vertical_sets[j] +
                      ': ' +
                      str(sets[j].mu(inputs[i])))
        return burn, thrust
