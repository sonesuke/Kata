from peak.rules import when


class Roll:

    def __init__(self, pins):
        if pins < 0:
            raise ValueError
        self.pins = pins

    def sweep(self, pins):
        return pins - self.pins

    def to_score(self):
        return Score(self.pins)


class Rolls:

    def __init__(self):
        self.rolls = []

    def append(self, roll):
        self.rolls.append(roll)

    def is_size_equal_to(self, size):
        return len(self.rolls) == size

    def apply_policy(self, policy):
        map(lambda x: policy.calc_score(x), self.rolls)

    def __add__(self, right_side):
        rolls = Rolls()
        rolls.rolls = self.rolls + right_side.rolls
        return rolls

    def take(self, count):
        rolls = Rolls()
        rolls.rolls = self.rolls[:count]
        return rolls


class Pins:

    def __init__(self):
        self.pins = 10
        self.served = False

    def accept(self, roll):
        if roll.sweep(self.pins) < 0:
            raise ValueError
        self.pins = roll.sweep(self.pins)

    def is_empty(self):
        return self.pins == 0

    def is_served(self):
        return self.served

    def serve(self):
        self.pins = 10
        self.served = True


class Frame:

    def __init__(self):
        self.rolls = Rolls()
        self.remain_pins = Pins()

    def apply_policy(self, policy):
        policy.calc_score(self.rolls)

    def append(self, roll):
        self.remain_pins.accept(roll)
        self.rolls.append(roll)

    def is_full(self):
        if self.remain_pins.is_empty():
            return True
        return self.rolls.is_size_equal_to(2)

    def is_empty(self):
        return self.remain_pins.is_empty()

    def is_size_equal_to(self, size):
        return self.rolls.is_size_equal_to(size)

    def accept(self, gather):
        gather.add(self.rolls)


class LastFrame:

    def __init__(self):
        self.rolls = Rolls()
        self.remain_pins = Pins()

    def apply_policy(self, policy):
        policy.calc_score(self.rolls)

    def append(self, roll):
        self.remain_pins.accept(roll)
        self.rolls.append(roll)
        self.serve_pins_as_necessary()

    def is_necessary_serve_pins(self):
        if self.rolls.is_size_equal_to(3):
            return False
        return self.remain_pins.is_empty()

    def serve_pins_as_necessary(self):
        if self.is_necessary_serve_pins():
            self.remain_pins.serve()

    def is_full(self):
        if self.remain_pins.is_served():
            return self.rolls.is_size_equal_to(3)
        return self.rolls.is_size_equal_to(2)

    def accept(self, gather):
        gather.add(self.rolls)


class RollGather:

    def __init__(self):
        self.rolls = Rolls()

    def visit(self, frame):
        frame.accept(self)

    def add(self, rolls):
        self.rolls += rolls

    def to_rolls(self):
        return self.rolls


class FrameFactory:

    @classmethod
    def create(cls, frame_index):
        return LastFrame() if frame_index == 9 else Frame()


class Frames:

    def __init__(self):
        self.frames = [FrameFactory.create(1)]

    def get_current_frame_index(self):
        return len(self.frames)

    def get_last_frame(self):
        return self.frames[-1]

    def create_next_frame(self):
        current_index = self.get_current_frame_index()
        self.frames += [FrameFactory.create(current_index)]

    def append(self, roll):
        self.get_last_frame().append(roll)
        if self.get_last_frame().is_full() and not self.is_max_frame():
            self.create_next_frame()

    def is_max_frame(self):
        return len(self.frames) == 10

    def is_full(self):
        return self.is_max_frame() and self.get_last_frame().is_full()

    def apply_policy(self, policy):
        map(lambda x: policy.calc_score(x), self.frames)

    def get_after_frames(self, frame):
        next_frame_index = self.frames.index(frame) + 1
        return self.frames[next_frame_index:]

    def get_rest_rolls(self, frame):
        g = RollGather()
        map(lambda x: g.visit(x), self.get_after_frames(frame))
        return g.to_rolls()


class Score:

    def __init__(self, value):
        self.value = value

    def to_number(self):
        return self.value

    def __add__(self, score):
        return Score(self.value + score.value)


class SweepPins:

    def __init__(self):
        self.score = Score(0)

    def calc_score(self, target):
        target.apply_policy(self)

    def to_score(self):
        return self.score

    @when(calc_score, (Roll,))
    def calc_score(self, roll):
        self.score += roll.to_score()


class Strike:

    def __init__(self):
        self.score = Score(0)
        self.frames = None

    def calc_score(self, target):
        target.apply_policy(self)

    def to_score(self):
        return self.score

    def is_strike(self, frame):
        if not frame.is_empty():
            return False
        return frame.is_size_equal_to(1)

    @when(calc_score, (Frames,))
    def calc_score(self, frames):
        self.frames = frames
        frames.apply_policy(self)

    @when(calc_score, (Frame,))
    def calc_score(self, frame):
        if self.is_strike(frame):
            self.calc_bonus(frame)

    @when(calc_score, (LastFrame,))
    def calc_score(self, frame):
        pass

    @when(calc_score, (Roll,))
    def calc_score(self, roll):
        self.score += roll.to_score()

    def calc_bonus(self, frame):
        rest_rolls = self.frames.get_rest_rolls(frame)
        bonus_rolls = rest_rolls.take(2)
        bonus_rolls.apply_policy(self)


class Spare:

    def __init__(self):
        self.score = Score(0)
        self.frames = None

    def calc_score(self, target):
        target.apply_policy(self)

    def to_score(self):
        return self.score

    def is_spare(self, frame):
        if not frame.is_empty():
            return False
        return not frame.is_size_equal_to(1)

    @when(calc_score, (Frames, ))
    def calc_score(self, frames):
        self.frames = frames
        frames.apply_policy(self)

    @when(calc_score, (Frame, ))
    def calc_score(self, frame):
        if self.is_spare(frame):
            self.calc_bonus(frame)

    @when(calc_score, (LastFrame,))
    def calc_score(self, frame):
        pass

    @when(calc_score, (Roll, ))
    def calc_score(self, roll):
        self.score += roll.to_score()

    def calc_bonus(self, frame):
        rest_rolls = self.frames.get_rest_rolls(frame)
        bonus_rolls = rest_rolls.take(1)
        bonus_rolls.apply_policy(self)


class PoliciesFacotry:
    @classmethod
    def create(cls):
        return [SweepPins(), Strike(), Spare()]


class Scorer:

    def __init__(self):
        self.policies = PoliciesFacotry.create()

    def calc_score(self, frames):
        map(lambda x: x.calc_score(frames), self.policies)
        return sum(map(lambda x: x.to_score(), self.policies), Score(0))


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        if self.frames.is_full():
            raise ValueError
        self.frames.append(Roll(pins))

    def get_current_frame_index(self):
        return self.frames.get_current_frame_index()

    def calc_score(self):
        s = Scorer()
        score = s.calc_score(self.frames)
        return score.to_number()
