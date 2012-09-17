

class Score:

    def __init__(self, score=0):
        self.score = score

    def __add__(self, rhs):
        return Score(self.score + rhs.score)

    @property
    def value(self):
        return self.score


class Frame:

    def __init__(self):
        self.rolls = []

    def is_full(self):
        if self.is_strike():
            return True
        return len(self.rolls) == 2

    def roll(self, pins):
        if pins > 10:
            raise ValueError
        if len(self.rolls) > 0:
            if self.rolls[-1] != 10 and self.rolls[-1] + pins > 10:
                raise ValueError
        self.rolls += [pins]

    @property
    def bonus_count(self):
        if self.is_spare():
            return 1
        if self.is_strike():
            return 2
        return 0

    def is_spare(self):
        if self.is_strike():
            return False
        return sum(self.rolls) == 10

    def is_strike(self):
        return sum(self.rolls[:1]) == 10

    def score(self, rolls):
        rolls = rolls.take_n(self.bonus_count)
        score = Score(sum(self.rolls))
        return score + rolls.score


class Frame10(Frame):

    def is_full(self):
        if sum(self.rolls[:1]) == 10:
            return len(self.rolls) == 3
        if sum(self.rolls[:2]) == 10:
            return len(self.rolls) == 3
        return len(self.rolls) == 2


class Roll:

    def __init__(self, pins):
        self.pins = pins

    @property
    def value(self):
        return self.pins

    @property
    def score(self):
        return Score(self.pins)


class Rolls:

    def __init__(self):
        self.rolls = []

    @classmethod
    def from_frames(cls, frames):
        rolls = Rolls()
        for f in frames:
            for r in f.rolls:
                rolls.rolls += [Roll(r)]
        return rolls

    def take_n(self, count):
        value = Rolls()
        value.rolls += self.rolls[:count]
        return value

    @property
    def score(self):
        return reduce(lambda x, y: x + y.score, self.rolls, Score())


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

    def last_frame_roll(self, pins):
        self.last_frame.roll(pins.value)

    @property
    def sum_score(self):
        f = lambda x, y: x + y.score(Rolls.from_frames(self.next_frame(y)))
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
