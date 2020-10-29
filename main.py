import sys
import random


def color_name(number):
    return COLORS[number]


COLORS = {0: "red", 1: "green", 2: "white", 3: "yellow", 4: "purple", 5: "blue"}

# NORTH-EAST-SOUTH-WEST
NEIGHBORS = {0: [4, 3, 5, 1], 1: [4, 0, 5, 2], 2: [4, 1, 5, 3], 3: [4, 2, 5, 0], 4: [2, 3, 0, 1], 5: [0, 3, 2, 1]}


class IsSelfException(Exception):
    pass


class IsOppositeSideException(Exception):
    pass


class Rubik:
    def __init__(self):
        self.top = Side(0)
        self.bottom = Side(2)
        self.west = Side(1)
        self.north = Side(4)
        self.east = Side(3)
        self.south = Side(5)

    def get_side(self, side):
        if side == 0: return self.top
        if side == 1: return self.west
        if side == 2: return self.bottom
        if side == 3: return self.east
        if side == 4: return self.north
        if side == 5: return self.south

    def is_solved(self):
        return self.top.is_solved() and self.bottom.is_solved() and self.west.is_solved() and self.east.is_solved() and self.north.is_solved() and self.south.is_solved()

    def correct_number(self):
        correct = 0
        for i in range(6):
            correct = correct + self.get_side(i).correct_number()
        return correct

    def validate(self):
        counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for i in range(6):
            s = self.get_side(i)
            for r in s.fields:
                for f in r:
                    counts[f] = counts[f] + 1
        return counts[0] == 9 and counts[1] == 9 and counts[2] == 9 and counts[3] == 9 and counts[4] == 9 and counts[5] == 9

    def __str__(self):
        res = "CUBE\n"
        for i in range(6):
            res = res + self.get_side(i).__str__() + "\n--------\n"
        return res

    def get_id(self):
        res = ""
        for i in range(6):
            s = self.get_side(i)
            for r in s.fields:
                for f in r:
                    res = res + f.__str__()
        return res

    def turn_counter_clock(self, side):
        old = self.__str__()
        self.get_side(side).rotate_counter_clock()
        north = self.get_side(NEIGHBORS[side][0])
        east = self.get_side(NEIGHBORS[side][1])
        south = self.get_side(NEIGHBORS[side][2])
        west = self.get_side(NEIGHBORS[side][3])

        n_row = north.get_neighboring_row(side)
        e_row = east.get_neighboring_row(side)
        s_row = south.get_neighboring_row(side)
        w_row = west.get_neighboring_row(side)

        north.set_neighboring_row(side, e_row)
        west.set_neighboring_row(side, n_row)
        south.set_neighboring_row(side, w_row)
        east.set_neighboring_row(side, s_row)
        if not self.validate():
            print("Turned side " + color_name(side) + " counter-clockwise.")
            print(old)
            print(self.__str__())

    def turn_clock(self, side):
        old = self.__str__()

        self.get_side(side).rotate_clock()
        north = self.get_side(NEIGHBORS[side][0])
        east = self.get_side(NEIGHBORS[side][1])
        south = self.get_side(NEIGHBORS[side][2])
        west = self.get_side(NEIGHBORS[side][3])

        n_row = north.get_neighboring_row(side)
        e_row = east.get_neighboring_row(side)
        s_row = south.get_neighboring_row(side)
        w_row = west.get_neighboring_row(side)

        north.set_neighboring_row(side, w_row)
        west.set_neighboring_row(side, s_row)
        south.set_neighboring_row(side, e_row)
        east.set_neighboring_row(side, n_row)
        if not self.validate():
            print("Turned side " + color_name(side) + " clockwise.")
            print(old)
            print(self.__str__())


class Side:
    def __init__(self, color):
        self.fields = [[color for i in range(3)] for j in range(3)]
        self.center = color

    def is_solved(self):
        for r in self.fields:
            for f in r:
                if f != self.center:
                    return False

        return True

    def correct_number(self):
        correct = 0
        for r in self.fields:
            for f in r:
                if f == self.center:
                    correct = correct + 1
        return correct

    def get_neighboring_row(self, color):
        if color == self.center:
            raise IsSelfException
        if not NEIGHBORS[self.center].__contains__(color):
            print(self.center)
            print(color)
            raise IsOppositeSideException
        if color == NEIGHBORS[self.center][0]:
            return self.fields[0]
        elif color == NEIGHBORS[self.center][1]:
            return [self.fields[0][2], self.fields[1][2], self.fields[2][2]]
        elif color == NEIGHBORS[self.center][2]:
            return [self.fields[2][0], self.fields[2][1], self.fields[2][2]]
        elif color == NEIGHBORS[self.center][3]:
            return [self.fields[0][0], self.fields[1][0], self.fields[2][0]]

    def set_neighboring_row(self, color, row):
        if color == self.center:
            raise IsSelfException
        if not NEIGHBORS[self.center].__contains__(color):
            raise IsOppositeSideException
        if color == NEIGHBORS[self.center][0]:
            self.fields[0] = row
        elif color == NEIGHBORS[self.center][1]:
            self.fields[0][2] = row[0]
            self.fields[1][2] = row[1]
            self.fields[2][2] = row[2]
        elif color == NEIGHBORS[self.center][2]:
            self.fields[2][0] = row[0]
            self.fields[2][1] = row[1]
            self.fields[2][2] = row[2]
        elif color == NEIGHBORS[self.center][3]:
            self.fields[0][0] = row[0]
            self.fields[1][0] = row[1]
            self.fields[2][0] = row[2]

    def rotate_clock(self):
        new = [[0 for i in range(3)] for j in range(3)]
        # oben
        new[0][0] = self.fields[2][0]
        new[0][1] = self.fields[1][0]
        new[0][2] = self.fields[0][0]
        # mitte
        new[1][0] = self.fields[2][1]
        new[1][1] = self.fields[1][1]
        new[1][2] = self.fields[0][1]
        # unten
        new[2][0] = self.fields[2][2]
        new[2][1] = self.fields[1][2]
        new[2][2] = self.fields[0][2]

        self.fields = new

    def rotate_counter_clock(self):
        new = [[0 for i in range(3)] for j in range(3)]
        # oben
        new[0][0] = self.fields[0][2]
        new[0][1] = self.fields[1][2]
        new[0][2] = self.fields[2][2]
        # mitte
        new[1][0] = self.fields[0][1]
        new[1][1] = self.fields[1][1]
        new[1][2] = self.fields[2][1]
        # unten
        new[2][0] = self.fields[0][0]
        new[2][1] = self.fields[1][0]
        new[2][2] = self.fields[2][0]

        self.fields = new

    def __str__(self):
        return self.fields[0].__str__() + "\n" + self.fields[1].__str__() + "\n" + self.fields[2].__str__()

#intialize cube
r = Rubik()

# shuffle cube
r.turn_counter_clock(0)
r.turn_counter_clock(1)
#r.turn_counter_clock(2)
#r.turn_counter_clock(3)
r.turn_counter_clock(4)
#r.turn_counter_clock(5)
#r.turn_clock(0)
#r.turn_clock(1)
#r.turn_clock(2)
#r.turn_clock(3)
#r.turn_clock(4)
#r.turn_clock(5)

#solvers

def dumb_solve(rubik, path=[], states=set()):
    for i in range(6):
        npath = path.copy()
        npath.append(i.__str__() + "l")
        rubik.turn_counter_clock(i)
        if states.__contains__(rubik.get_id()):
            rubik.turn_clock(i)
        else:
            states.add(rubik.get_id())
            if rubik.is_solved():
                print("------------")
                print(len(npath))
                print(npath)
                # revert change
                rubik.turn_clock(i)
                return True
            else:
                if dumb_solve(rubik, path=npath, states=states):
                    return True
                else:
                    rubik.turn_counter_clock(i)

        npath = path.copy()
        npath.append(i.__str__() + "r")
        rubik.turn_clock(i)
        if states.__contains__(rubik.get_id()):
            rubik.turn_clock(i)
        else:
            states.add(rubik.get_id())
            if rubik.is_solved():
                print("------------")
                print(len(path))
                print(path)
                # revert change
                rubik.turn_counter_clock(i)
                return True
            else:
                if dumb_solve(rubik, path=npath, states=states):
                    return True
                else:
                    rubik.turn_counter_clock(i)

    print("Done!")

# dumb random algorithm that does not work
def rand_solve(rubik, path=[], states=set()):
    dir = random.randint(0, 1)
    side = random.randint(0,5)
    if dir == 0:
        rubik.turn_counter_clock(side)
        if states.__contains__(rubik.get_id()):
            rubik.turn_clock(side)
        else:
            states.add(rubik.get_id())
            path.append(side.__str__() + "l")
    else:
        rubik.turn_clock(side)
        if states.__contains__(rubik.get_id()):
            rubik.turn_counter_clock(side)
        else:
            states.add(rubik.get_id())
            path.append(side.__str__() + "r")
    if rubik.is_solved():
        print(len(path))
        print(path)

    return [dir, side]

def correctify_solve(rubik, path=[], states=[]):
    best = [-1, -1, rubik.correct_number()]
    for dir in [0,1]:
        for side in range(5):
            if dir == 0:
                rubik.turn_counter_clock(side)
                if states.__contains__(rubik.get_id()):
                    rubik.turn_clock(side)
                else:
                    states.add(rubik.get_id())
                    val = rubik.correct_number()
                    if (val >= best[2]):
                        best[2] = val
                        best[0] = dir
                        best[1] = side
                    rubik.turn_clock(side)

            else:
                rubik.turn_clock(side)
                if states.__contains__(rubik.get_id()):
                    rubik.turn_counter_clock(side)
                else:
                    states.add(rubik.get_id())
                    val = rubik.correct_number()
                    if (val >= best[2]):
                        best[2] = val
                        best[0] = dir
                        best[1] = side
                    rubik.turn_counter_clock(side)

    if best[0] == -1:

        #Try random 3 steps
        correct = rubik.correct_number()
        for i in range(3):
            npath = path.copy()
            steps = []
            steps.append(rand_solve(rubik, path=npath, states=states))
            steps.append(rand_solve(rubik, path=npath, states=states))
            steps.append(rand_solve(rubik, path=npath, states=states))
            n_correct = rubik.correct_number()
            if n_correct <= correct:
                steps.reverse()
                for step in steps:
                    if step[0] == 0:
                        rubik.turn_clock(step[1])
                    else:
                        rubik.turn_counter_clock(step[1])
            else:
                break

        if n_correct <= correct:
            print(rubik)
            print(npath)
            print("Correct:")
            print(rubik.correct_number())
            return False
        return correctify_solve(rubik, path=npath, states=states)

    dir = best[0]
    side = best[1]

    if dir == 0:
        rubik.turn_counter_clock(side)
        path.append(side.__str__() + "l")
        print(side.__str__() + "l")

    else:
        rubik.turn_clock(side)
        path.append(side.__str__() + "r")
        print(side.__str__() + "r")

    if rubik.is_solved():
        print("SOLVED")
        print(path)
        return True
    else:
        return correctify_solve(rubik, path=path, states=states)




sys.setrecursionlimit(100100)
states = set()
states.add(r.get_id())
#dumb_solve(r, states=states)

states = set()
states.add(r.get_id())
#rand_solve(r, states)
correctify_solve(r, states=states)