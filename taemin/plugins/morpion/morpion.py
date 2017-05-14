""" Morpion game """

class Morpion(object):
    """ Morpion object, contain a game """

    def __init__(self, size=3):
        self.size = size
        self.matrix = [
            [None]*size for _ in range(size)
        ]

    def reset(self):
        """ Reset the game"""
        self.__init__(self.size)

    def winner(self):
        """ Try to find the winner of the game """

        for line in self.iter_all():
            line_set = set(line)
            if len(line_set) == 1 and line_set != {None}:
                return line[0]

    def iter_line(self):
        """ iter on each line of the game """

        for line in self.matrix:
            yield line

    def play(self, line, col, value):
        """ Place an element in the morpion """

        if line >= self.size or line < 0:
            return False

        if col >= self.size or col < 0:
            return False

        if self.matrix[line][col] is not None:
            return False

        self.matrix[line][col] = value

        return True

    def iter_column(self):
        """ iter on each column of the game """
        for i in range(self.size):
            yield [self.matrix[j][i] for j in range(self.size)]

    def iter_diagonal(self):
        """ iter on each column of the game """
        yield [self.matrix[i][i] for i in range(self.size)]

        yield [self.matrix[self.size - 1 - i][i] for i in range(self.size)]

    def iter_all(self):
        """ Iterate over line, column, and diagonal """
        yield from self.iter_line()
        yield from self.iter_column()
        yield from self.iter_diagonal()
