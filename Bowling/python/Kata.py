

class Score:

    def __init__(self, value=0):
        self.score = value

    def __add__(self, rhs):
        return Score(self.score + rhs.score)

    @property
    def value(self):
        return self.score

    def is_10(self):
        return self.score == 10


class Roll:

    def __init__(self, pins=0):
        if pins < 0 or 10 < pins:
            raise ValueError
        self.roll = pins

    @property
    def score(self):
        return Score(self.roll)

    def is_under_10(self):
        return self.roll < 10

    def validate_10_over_added_with(self, roll):
        if roll is None:
            return
        Roll(self.roll + roll.roll)


class Rolls:

    def __init__(self):
        self.rolls = []

    def add(self, roll):
        self.rolls += [roll]

    def take(self, length):
        r = Rolls()
        r.rolls = self.rolls[:length]
        return r

    def calc_score(self):
        return sum(map(lambda x: x.score, self.rolls), Score())

    @property
    def length(self):
        return len(self.rolls)

    def is_10(self):
        return self.calc_score().is_10()

    def __add__(self, rolls):
        r = Rolls()
        r.rolls = self.rolls + rolls.rolls
        return r

    @property
    def last_roll(self):
        if len(self.rolls) == 0:
            return None
        return self.rolls[-1]

    def last_roll_is_under_10(self):
        if self.last_roll is None:
            return True
        return self.last_roll.is_under_10()


class Frame:

    def __init__(self):
        self.rolls = Rolls()

    def roll(self, roll):
        self.validate_over_pins_in_a_frame(roll)
        self.rolls.add(roll)

    def validate_over_pins_in_a_frame(self, roll):
        if not self.rolls.last_roll_is_under_10():
            return
        roll.validate_10_over_added_with(self.rolls.last_roll)

    def is_strike(self):
        rolls = self.rolls.take(1)
        return rolls.is_10()

    def is_spare(self):
        rolls = self.rolls.take(2)
        return rolls.is_10()

    def is_full(self):
        if self.is_strike():
            return True
        return self.rolls.length == 2

    @property
    def bonus_count(self):
        if self.is_strike():
            return 2
        return 1 if self.is_spare() else 0

    def calc_bonus(self, rest_rolls):
        rolls = rest_rolls.take(self.bonus_count)
        return rolls.calc_score()

    def calc_score(self, rest_rolls):
        score = self.calc_bonus(rest_rolls)
        return score + self.rolls.calc_score()

    def accept(self, gatherer):
        gatherer.add(self.rolls)


class Frame10(Frame):

    def is_full(self):
        if self.is_strike() or self.is_spare():
            return self.rolls.length == 3
        return self.rolls.length == 2


class RollGatherer:

    def __init__(self):
        self.rolls = Rolls()

    def visit(self, frame):
        frame.accept(self)

    def add(self, rolls):
        self.rolls += rolls

    @property
    def result(self):
        return self.rolls


class Frames:

    def __init__(self):
        self.frames = []

    def last_frame_is_full(self):
        if self.last_frame is None:
            return True
        return self.last_frame.is_full()

    def create_frame(self):
        if len(self.frames) == 10:
            raise ValueError
        self.frames += [Frame()] if len(self.frames) < 9 else [Frame10()]

    @property
    def last_frame(self):
        if len(self.frames) == 0:
            return None
        return self.frames[-1]

    def roll(self, roll):
        if self.last_frame_is_full():
            self.create_frame()
        self.last_frame.roll(roll)

    def rest_rolls(self, frame):
        g = RollGatherer()
        map(lambda x: g.visit(x), self.frames[self.frames.index(frame) + 1:])
        return g.result

    def calc_score(self):
        calc_score = lambda x: x.calc_score(self.rest_rolls(x))
        score = sum(map(lambda x: calc_score(x), self.frames), Score())
        return score


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        self.frames.roll(Roll(pins))

    def calc_score(self):
        score = self.frames.calc_score()
        return score.value
