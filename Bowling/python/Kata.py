

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

    def append(self, roll):
        self.rolls.append(roll)

    def __len__(self):
        return len(self.rolls)

    def __add__(self, rhs):
        rolls = Rolls()
        rolls.rolls = self.rolls + rhs.rolls
        return rolls

    def __iter__(self):
        for r in self.rolls:
            yield r

    def take(self, count):
        rolls = Rolls()
        rolls.rolls = self.rolls[:count]
        return rolls


class RemainPins:

    def __init__(self):
        self.pins = 10
        self.reseted = False

    def knock_down_by(self, roll):
        if roll.knock_down(self.pins) < 0:
            raise ValueError
        self.pins = roll.knock_down(self.pins)

    def reset(self):
        self.pins = 10
        self.reseted = True

    def is_empty(self):
        return self.pins == 0

    def is_reseted(self):
        return self.reseted


class Frame:

    def __init__(self):
        self.rolls = Rolls()
        self.remain_pins = RemainPins()

    def append(self, roll):
        self.remain_pins.knock_down_by(roll)
        self.rolls.append(roll)

    def is_full(self):
        if self.remain_pins.is_empty():
            return True
        return len(self.rolls) == 2

    def accept(self, gather):
        gather.add(self.rolls)

    def is_empty(self):
        return self.remain_pins.is_empty()

    def is_one_roll(self):
        return len(self.rolls) == 1


class LastFrame:

    def __init__(self):
        self.remain_pins = RemainPins()
        self.rolls = Rolls()

    def append(self, roll):
        self.remain_pins.knock_down_by(roll)
        self.rolls.append(roll)
        self.reset_remain_pins_if_empy()

    def reset_remain_pins_if_empy(self):
        if self.remain_pins.is_empty():
            self.remain_pins.reset()

    def is_full(self):
        if self.remain_pins.is_reseted():
            return len(self.rolls) == 3
        return len(self.rolls) == 2

    def accept(self, gather):
        gather.add(self.rolls)

    def is_empty(self):
        return self.remain_pins.is_empty()

    def is_one_roll(self):
        return len(self.rolls) == 1


class FrameFactory:

    @classmethod
    def create(cls, frame_index):
        if frame_index == 10:
            return LastFrame()
        return Frame()


class Frames:

    def __init__(self):
        self.frames = []
        self.create_next_frame()

    def get_rest_frames(self, frame):
        index = self.frames.index(frame)
        return self.frames[index + 1:]

    def get_last_frame(self):
        return self.frames[-1]

    def append(self, roll):
        self.get_last_frame().append(roll)
        if self.get_last_frame().is_full() and self.is_not_max_frame():
            self.create_next_frame()

    def create_next_frame(self):
        next_frame_index = len(self.frames) + 1
        self.frames += [FrameFactory.create(next_frame_index)]

    def is_full(self):
        if self.is_not_max_frame():
            return False
        return self.get_last_frame().is_full()

    def is_not_max_frame(self):
        return len(self.frames) != 10

    def __iter__(self):
        for f in self.frames:
            yield f


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
        rolls = self.get_all_rolls(frames)
        return sum(map(lambda x: Score(x.to_pins()), rolls), Score(0))

    def get_all_rolls(self, frames):
        g = RollGather()
        map(lambda x: g.visit(x), frames)
        return g.to_rolls()


class BonusScoringRule:

    def __init__(self, is_bonus_frame, bonus_count):
        self.is_bonus_frame = is_bonus_frame
        self.bonus_count = bonus_count

    def calc_score(self, frames):
        self.frames = frames
        bonus_frames = [f for f in self.frames if self.is_bonus_frame(f)]
        return sum(map(lambda x: self.calc_bonus(x), bonus_frames), Score(0))

    def calc_bonus(self, frame):
        rolls = self.get_rest_roll(frame)
        bonus_rolls = rolls.take(self.bonus_count)
        return sum(map(lambda r: Score(r.to_pins()), bonus_rolls), Score(0))

    def get_rest_roll(self, frame):
        gather = RollGather()
        map(lambda x: gather.visit(x), self.frames.get_rest_frames(frame))
        return gather.to_rolls()


class ScoringRules:

    def __init__(self):
        self.rules = [NormalScoringRule()]
        self.rules.append(self.create_spare_rule())
        self.rules.append(self.create_strike_rule())

    def create_spare_rule(self):
        is_spare = lambda f: f.is_empty() and not f.is_one_roll()
        return BonusScoringRule(is_spare, 1)

    def create_strike_rule(self):
        is_strike = lambda f: f.is_empty() and f.is_one_roll()
        return BonusScoringRule(is_strike, 2)

    def __iter__(self):
        for rule in self.rules:
            yield rule


class Scorer:

    @classmethod
    def calc_score(cls, frames):
        scores = map(lambda rule: rule.calc_score(frames), ScoringRules())
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
