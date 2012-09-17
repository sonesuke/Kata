

class Score:

    def __init__(self, score=0):
        self.score = score

    def __add__(self, rhs):
        return Score(self.score + rhs.score)

    @property
    def value(self):
        return self.score


class Roll:

    def __init__(self, pins=0):
        if pins > 10:
            raise ValueError
        self.pins = pins

    @property
    def value(self):
        return self.pins

    @property
    def score(self):
        return Score(self.pins)

    def is_10(self):
        return self.pins == 10

    def is_over(self):
        return self.pins > 10

    def __add__(self, rhs):
        return Roll(self.pins + rhs.pins)


class Rolls:

    def __init__(self, rolls=None):
        self.rolls = rolls if not rolls is None else []

    @classmethod
    def from_frames(cls, frames):
        return Rolls(reduce(lambda x, y: x + y.rolls.rolls, frames, []))

    def take_n(self, count):
        return Rolls(self.rolls[:count])

    @property
    def score(self):
        return reduce(lambda x, y: x + y.score, self.rolls, Score())

    def size_equal_to(self, size):
        return len(self.rolls) == size

    def is_spare(self):
        if self.is_strike():
            return False
        return reduce(lambda x, y: x + y, self.rolls[:2], Roll()).is_10()

    def is_strike(self):
        return reduce(lambda x, y: x + y, self.rolls[:1], Roll()).is_10()

    @property
    def last_roll(self):
        return self.rolls[-1]

    def over_10_in_continuous(self, roll):
        if len(self.rolls) == 0:
            return False
        return not self.last_roll.is_10() and (self.last_roll + roll).is_over()

    def append(self, roll):
        self.rolls += [roll]


class Frame:

    def __init__(self):
        self.rolls = Rolls()

    def is_full(self):
        if self.rolls.is_strike():
            return True
        return self.rolls.size_equal_to(2)

    def roll(self, roll):
        if self.rolls.over_10_in_continuous(roll):
            raise ValueError
        self.rolls.append(roll)

    @property
    def bonus_count(self):
        if self.rolls.is_spare():
            return 1
        return 2 if self.rolls.is_strike() else 0

    def score(self, rolls):
        rolls = rolls.take_n(self.bonus_count)
        score = self.rolls.score
        return score + rolls.score


class Frame10(Frame):

    def is_full(self):
        if self.rolls.is_strike() or self.rolls.is_spare():
            return self.rolls.size_equal_to(3)
        return self.rolls.size_equal_to(2)


class Frames:

    def __init__(self):
        self.frames = [Frame()]

    @property
    def last_frame(self):
        return self.frames[-1]

    def last_frame_is_full(self):
        return self.last_frame.is_full()

    def create_next(self):
        if len(self.frames) == 10:
            raise ValueError
        return Frame10() if len(self.frames) == 9 else Frame()

    def create_frame(self):
        self.frames += [self.create_next()]

    def last_frame_roll(self, roll):
        self.last_frame.roll(roll)

    @property
    def sum_score(self):
        remain_rolls = lambda x: Rolls.from_frames(self.next_frame(x))
        f = lambda x, y: x + y.score(remain_rolls(y))
        return reduce(f, self.frames, Score())

    def next_frame(self, frame):
        idx = self.frames.index(frame)
        return self.frames[idx + 1:]


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        if self.frames.last_frame_is_full():
            self.frames.create_frame()
        self.frames.last_frame_roll(Roll(pins))

    @property
    def score(self):
        score = self.frames.sum_score
        return score.value
