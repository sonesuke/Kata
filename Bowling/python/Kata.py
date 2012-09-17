

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


class Game:

    def __init__(self):
        self.frames = [Frame()]

    def roll(self, pins):
        if self.frames[-1].is_full():
            if len(self.frames) == 9:
                self.frames += [Frame10()]
            elif len(self.frames) < 9:
                self.frames += [Frame()]
            else:
                raise ValueError
        self.frames[-1].roll(pins)

    @property
    def score(self):
        val = sum(map(lambda x: x.score, self.frames))
        for idx in range(len(self.frames)):
            val += self.bonus(idx + 1, self.frames[idx].bonus_count)
        return val

    def bonus(self, idx, bonus_count):
        rolls = reduce(lambda x, y: x + y.rolls, self.frames[idx:], [])
        return sum(rolls[:bonus_count])
