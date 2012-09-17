

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
    def score(self):
        return sum(self.rolls)

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


class Score:

    def __init__(self, score):
        self.score = score

    @property
    def value(self):
        return self.score

    def add(self, score):
        self.score += score.value


class Frames:

    def __init__(self):
        self.frames = [Frame()]

    def last_frame_is_full(self):
        return self.frames[-1].is_full()

    def create_frame(self):
        if len(self.frames) == 9:
            self.frames += [Frame10()]
        elif len(self.frames) < 9:
            self.frames += [Frame()]
        else:
            raise ValueError

    def last_frame_roll(self, pins):
        self.frames[-1].roll(pins.value)

    @property
    def sum_score(self):
        return Score(sum(map(lambda x: x.score, self.frames)))

    @property
    def sum_bonus(self):
        return self.add_bonus(0)

    def add_bonus(self, val):
        for idx in range(len(self.frames)):
            val += self.each_bonus(idx + 1, self.frames[idx].bonus_count)
        return Score(val)

    def each_bonus(self, idx, bonus_count):
        rolls = reduce(lambda x, y: x + y.rolls, self.frames[idx:], [])
        return sum(rolls[:bonus_count])


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        if self.frames.last_frame_is_full():
            self.frames.create_frame()
        self.frames.last_frame_roll(Roll(pins))

    @property
    def score(self):
        s = self.frames.sum_score
        s.add(self.frames.sum_bonus)
        return s.value
