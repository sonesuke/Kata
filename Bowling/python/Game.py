class Frame:

    def __init__(self):
        self.rolls = []
        self.next_frame = None

    def is_full(self):
        if self.is_strike():
            return True
        return len(self.rolls) >= 2

    def add(self, pins):
        if sum(self.rolls + [pins]) > 10:
            raise ValueError
        self.rolls += [pins]

    def is_spare(self):
        if len(self.rolls) != 2:
            return False
        return sum(self.rolls[:2]) == 10

    def is_strike(self):
        return len(self.rolls) == 1 and self.rolls[0] == 10

    @property
    def score(self):
        ret = sum(self.rolls)
        if self.next_frame:
            if self.is_spare():
                ret += sum(self.next_frame.rolls[:1])
            if self.is_strike():
                ret += sum(self.next_frame.rolls[:2])
        return ret


class Frame10(Frame):
    def is_full(self):
        if sum(self.rolls[:2]) >= 10:
            return 3 <= len(self.rolls)
        else:
            return 2 <= len(self.rolls)

    def add(self, pins):
        if pins > 10:
            raise ValueError
        if len(self.rolls) == 1:
            if self.rolls[0] < 10 and self.rolls[0] + pins > 10:
                raise ValueError
        self.rolls += [pins]

    @property
    def score(self):
        ret = sum(self.rolls)
        if self.rolls[0]:
            if self.rolls[0] != 10 and sum(self.rolls[0:2]) == 10:
                ret += sum(self.rolls[2:3])
            if self.rolls[0] == 10:
                ret += sum(self.rolls[1:3])
        return ret


class Game:

    def __init__(self):
        self.frames = [Frame()]

    def roll(self, pins):
        if self.frames[-1].is_full():
            if len(self.frames) < 9:
                self.frames += [Frame()]
            elif len(self.frames) == 9:
                self.frames += [Frame10()]
            else:
                raise ValueError
            self.frames[-2].next_frame = self.frames[-1]
        self.frames[-1].add(pins)

    @property
    def score(self):
        return reduce(lambda x, y: x + y.score, self.frames, 0)
