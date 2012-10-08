

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

    def __init__(self):
        self.rolls = []

    def __len__(self):
        return len(self.rolls)

    def append(self, roll):
        self.rolls.append(roll)

    def __add__(self, rhs):
        rs = Rolls()
        rs.rolls = self.rolls + rhs.rolls
        return rs

    def __iter__(self):
        for roll in self.rolls:
            yield roll

    def take(self, count):
        rs = Rolls()
        rs.rolls = self.rolls[:count]
        return rs


class RemainPins:

    def __init__(self):
        self.pins = 10
        self.reseted = False

    def is_empty(self):
        return self.pins == 0

    def knock_down_by(self, roll):
        if roll.knock_down(self.pins) < 0:
            raise ValueError
        self.pins = roll.knock_down(self.pins)

    def is_reseted(self):
        return self.reseted

    def reset_if_empty(self):
        if self.is_empty():
            self.pins = 10
            self.reseted = True


class Frame:

    def __init__(self):
        self.remain_pins = RemainPins()
        self.rolls = Rolls()

    def is_full(self):
        if self.remain_pins.is_empty():
            return True
        return len(self.rolls) == 2

    def append(self, roll):
        self.remain_pins.knock_down_by(roll)
        self.rolls.append(roll)

    def accept(self, gather):
        gather.add(self.rolls)

    def is_empty(self):
        return self.remain_pins.is_empty()

    def is_one_roll(self):
        return len(self.rolls) == 1


class LastFrame:

    def __init__(self):
        self.rolls = Rolls()
        self.remain_pins = RemainPins()

    def is_full(self):
        if self.remain_pins.is_reseted():
            return len(self.rolls) == 3
        return len(self.rolls) == 2

    def append(self, roll):
        self.remain_pins.knock_down_by(roll)
        self.rolls.append(roll)
        self.remain_pins.reset_if_empty()

    def accept(self, gather):
        gather.add(self.rolls)

    def is_empty(self):
        return self.remain_pins.is_empty()

    def is_one_roll(self):
        return len(self.rolls) == 1


class FrameFactory:

    @classmethod
    def create(cls, frame_index):
        return Frame() if frame_index < 10 else LastFrame()


class Frames:

    def __init__(self):
        self.frames = []
        self.create_next_frame()

    def get_last_frame(self):
        return self.frames[-1]

    def create_next_frame(self):
        self.frames += [FrameFactory.create(len(self.frames) + 1)]

    def append(self, roll):
        self.get_last_frame().append(roll)
        if self.get_last_frame().is_full() and self.is_not_max_frame():
            self.create_next_frame()

    def is_full(self):
        if self.is_not_max_frame():
            return False
        return self.get_last_frame().is_full()

    def is_not_max_frame(self):
        return len(self.frames) != 10

    def __iter__(self):
        for frame in self.frames:
            yield frame

    def get_rest_frames(self, frame):
        frames = Frames()
        frames.frames = self.frames[self.frames.index(frame) + 1:]
        return frames


class Score:

    def __init__(self, value):
        self.value = value

    def to_number(self):
        return self.value

    def __add__(self, rhs):
        return Score(self.value + rhs.value)


class RollGather:

    def __init__(self):
        self.rolls = Rolls()

    def visit(self, frame):
        frame.accept(self)

    def add(self, rolls):
        self.rolls += rolls

    def to_rolls(self):
        return self.rolls


class NormalScoringRule:

    def calc_score(self, frames):
        rolls = self.gather_all_rolls(frames)
        return sum(map(lambda r: Score(r.to_pins()), rolls), Score(0))

    def gather_all_rolls(self, frames):
        gather = RollGather()
        map(lambda f: gather.visit(f), frames)
        return gather.to_rolls()


class BonusScoringRule:

    def __init__(self, is_bonus_frame, bonus_count):
        self.is_bonus_frame = is_bonus_frame
        self.bonus_count = bonus_count

    def calc_score(self, frames):
        self.frames = frames
        bonus_frames = [f for f in frames if self.is_bonus_frame(f)]
        return sum(map(lambda f: self.calc_bonus(f), bonus_frames), Score(0))

    def calc_bonus(self, frame):
        rest_rolls = self.get_rest_rolls(frame)
        bonus_rolls = rest_rolls.take(self.bonus_count)
        return sum(map(lambda r: Score(r.to_pins()), bonus_rolls), Score(0))

    def get_rest_rolls(self, frame):
        gather = RollGather()
        map(lambda f: gather.visit(f), self.frames.get_rest_frames(frame))
        return gather.to_rolls()


class ScoringRules:

    def __init__(self):
        self.rules = [NormalScoringRule()]
        self.rules += [self.create_spare_rule()]
        self.rules += [self.create_strike_rule()]

    def __iter__(self):
        for rule in self.rules:
            yield rule

    def create_spare_rule(self):
        def is_bonus_frame(frame):
            return frame.is_empty() and not frame.is_one_roll()
        return BonusScoringRule(is_bonus_frame, 1)

    def create_strike_rule(self):
        def is_bonus_frame(frame):
            return frame.is_empty() and frame.is_one_roll()
        return BonusScoringRule(is_bonus_frame, 2)


class Scorer:

    @classmethod
    def calc_score(cls, frames):
        scores = map(lambda r: r.calc_score(frames), ScoringRules())
        score = sum(scores, Score(0))
        return score


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
