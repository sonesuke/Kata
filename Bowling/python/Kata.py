

class Roll:

    def __init__(self, pins):
        if pins < 0:
            raise ValueError
        self.pins = pins

    def to_pins(self):
        return self.pins

    def knock_down(self, pins):
        return pins - self.pins


class PinsServer:

    @classmethod
    def serve(cls):
        return 10


class RemainPins:

    def __init__(self, reset_policy):
        self.pins = PinsServer.serve()
        self.reset_policy = reset_policy

    def knock_down_by(self, roll):
        if roll.knock_down(self.pins) < 0:
            raise ValueError
        self.update_by(roll)

    def update_by(self, roll):
        self.pins = roll.knock_down(self.pins)
        self.pins = self.reset_policy(self.pins)

    def is_reseted(self):
        return self.reset_policy.is_reseted()

    def is_empty(self):
        return self.pins == 0


class NotResetIfEmpty:

    def __call__(self, pins):
        return pins

    def is_reseted(self):
        return False


class ResetIfEmpty:

    def __init__(self):
        self.reseted = False

    def __call__(self, pins):
        return self.reset() if pins == 0 else pins

    def reset(self):
        self.reseted = True
        return PinsServer.serve()

    def is_reseted(self):
        return self.reseted


class Rolls:

    def __init__(self, rolls=None):
        self.rolls = [] if rolls is None else rolls

    def append(self, roll):
        self.rolls.append(roll)

    def __len__(self):
        return len(self.rolls)

    def __iter__(self):
        for r in self.rolls:
            yield r

    def __add__(self, rhs):
        return Rolls(self.rolls + rhs.rolls)

    def take(self, count):
        return Rolls(self.rolls[:count])


class Frame:

    def __init__(self, remain_pins, is_full_policy):
        self.remain_pins = remain_pins
        self.is_full_policy = is_full_policy
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


class IsFullWithBonusRoll:

    def __call__(self, remain_pins, rolls):
        return len(rolls) == 3 if remain_pins.is_reseted() else len(rolls) == 2


class FrameFactory:

    @classmethod
    def create(cls, frame_index):
        if frame_index == 10:
            return Frame(RemainPins(ResetIfEmpty()), IsFullWithBonusRoll())
        return Frame(RemainPins(NotResetIfEmpty()), IsFull())


class Frames:

    def __init__(self):
        self.frames = []
        self.setup_next()

    def setup_next(self):
        next_frame_index = len(self.frames) + 1
        self.frames += [FrameFactory.create(next_frame_index)]

    def append(self, roll):
        self.last().append(roll)
        if self.last().is_full() and not self.is_max():
            self.setup_next()

    def last(self):
        return self.frames[-1]

    def is_max(self):
        return len(self.frames) == 10

    def is_full(self):
        return False if not self.is_max() else self.last().is_full()

    def __iter__(self):
        for f in self.frames:
            yield f

    def rests(self, frame):
        fs = Frames()
        fs.frames = self.frames[self.frames.index(frame) + 1:]
        return fs


class RollGather:

    def __init__(self):
        self.rolls = Rolls()

    def gather_all_rolls(self, frames):
        [self.visit(f) for f in frames]
        return self.rolls

    def visit(self, frame):
        frame.accept(self)

    def add(self, rolls):
        self.rolls += rolls


class NormalScoringRule:

    def calc_score(self, frames):
        rolls = RollGather().gather_all_rolls(frames)
        return sum([Score(r.to_pins()) for r in rolls], Score(0))


class BonusScoringRule:

    def __init__(self, is_bonus_frame, bonus_count):
        self.is_bonus_frame = is_bonus_frame
        self.bonus_count = bonus_count

    def calc_score(self, frames):
        self.frames = frames
        bonus_frames = [f for f in frames if self.is_bonus_frame(f)]
        return sum([self.calc_bonus(f) for f in bonus_frames], Score(0))

    def calc_bonus(self, frame):
        rest_frames = self.frames.rests(frame)
        bonus_rolls = self.gather_bonus_rolls(rest_frames)
        return sum([Score(r.to_pins()) for r in bonus_rolls], Score(0))

    def gather_bonus_rolls(self, rest_frames):
        rolls = RollGather().gather_all_rolls(rest_frames)
        return rolls.take(self.bonus_count)


class IsSpare:

    def __call__(self, frame):
        return frame.is_empty() and not frame.is_one_roll()


class IsStrike:

    def __call__(self, frame):
        return frame.is_empty() and frame.is_one_roll()


class Score:

    def __init__(self, value):
        self.value = value

    def to_number(self):
        return self.value

    def __add__(self, rhs):
        return Score(self.value + rhs.value)


class ScoringRules:

    def __init__(self):
        self.rules = [NormalScoringRule()]
        self.rules += [BonusScoringRule(IsSpare(), 1)]
        self.rules += [BonusScoringRule(IsStrike(), 2)]

    def __iter__(self):
        for r in self.rules:
            yield r


class Scorer:

    @classmethod
    def calc_score(cls, frames):
        rules = ScoringRules()
        return sum([r.calc_score(frames) for r in rules], Score(0))


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        if self.frames.is_full():
            raise ValueError
        self.frames.append(Roll(pins))

    def calc_score(self):
        score = Scorer.calc_score(self.frames)
        return score.to_number()
