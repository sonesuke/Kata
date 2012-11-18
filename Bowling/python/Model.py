

class Roll:

    def __init__(self, pins):
        if pins < 0:
            raise ValueError
        self.pins = pins

    def knock_down(self, pins):
        return pins - self.pins

    def to_pins(self):
        return self.pins


class Rolls:

    def __init__(self, rolls=None):
        self.rolls = [] if rolls is None else rolls

    def append(self, roll):
        self.rolls.append(roll)

    def __len__(self):
        return len(self.rolls)

    def __add__(self, rhs):
        return Rolls(self.rolls + rhs.rolls)

    def __iter__(self):
        for r in self.rolls:
            yield r

    def take(self, count):
        return Rolls(self.rolls[:count])


class PinServer:

    @classmethod
    def serve(cls):
        return 10


class RemainPins:

    def __init__(self, reset_policy):
        self.pins = PinServer.serve()
        self.reset_policy = reset_policy

    def knock_down_by(self, roll):
        if roll.knock_down(self.pins) < 0:
            raise ValueError
        self.update_by(roll)

    def update_by(self, roll):
        self.pins = roll.knock_down(self.pins)
        self.pins = self.reset_policy.update(self.pins)

    def is_empty(self):
        return self.pins == 0

    def is_reseted(self):
        return self.reset_policy.is_reseted()


class NotResetIfEmpty:

    def update(self, pins):
        return pins

    def is_reseted(self):
        return False


class ResetIfEmpty:

    def __init__(self):
        self.reseted = False

    def update(self, pins):
        return self.reset() if pins == 0 else pins

    def reset(self):
        self.reseted = True
        return PinServer.serve()

    def is_reseted(self):
        return self.reseted


class Frame:

    def __init__(self, remain_pins, is_full_policy):
        self.is_full_policy = is_full_policy
        self.remain_pins = remain_pins
        self.rolls = Rolls()

    def append(self, roll):
        self.remain_pins.knock_down_by(roll)
        self.rolls.append(roll)

    def is_full(self):
        return self.is_full_policy(self.remain_pins, self.rolls)

    def accept(self, gather):
        gather.add(self.rolls)

    def is_empty(self):
        return self.remain_pins.is_empty()

    def is_one_roll(self):
        return len(self.rolls) == 1


class IsFull:

    def __call__(self, remain_pins, rolls):
        return True if remain_pins.is_empty() else len(rolls) == 2


class IsFullWithBonus:

    def __call__(self, remain_pins, rolls):
        return len(rolls) == 3 if remain_pins.is_reseted() else len(rolls) == 2


class FrameFactory:

    @classmethod
    def create(cls, frame_index):
        if frame_index == 10:
            return Frame(RemainPins(ResetIfEmpty()), IsFullWithBonus())
        return Frame(RemainPins(NotResetIfEmpty()), IsFull())


class Frames:

    def __init__(self):
        self.frames = []
        self.create_frame()

    def rest(self, frame):
        fs = Frames()
        fs.frames = self.frames[self.frames.index(frame) + 1:]
        return fs

    def create_frame(self):
        next_frame_index = len(self.frames) + 1
        self.frames += [FrameFactory.create(next_frame_index)]

    def append(self, roll):
        self.last().append(roll)
        if self.last().is_full() and not self.is_max():
            self.create_frame()

    def is_full(self):
        if not self.is_max():
            return False
        return self.last().is_full()

    def is_max(self):
        return len(self.frames) == 10

    def last(self):
        return self.frames[-1]

    def __iter__(self):
        for f in self.frames:
            yield f

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, key):
        fs = Frames()
        fs.frames = self.frames[key]
        return fs


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        if self.frames.is_full():
            raise ValueError
        self.frames.append(Roll(pins))
