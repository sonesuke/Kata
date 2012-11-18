from Model import Rolls


class RollGather:

    def __init__(self):
        self.rolls = Rolls()

    def gather_by(self, frames):
        [self.visit(f) for f in frames]
        return self.rolls

    def visit(self, frame):
        frame.accept(self)

    def add(self, rolls):
        self.rolls += rolls


class NormalScoringRules:

    def calc_score(self, frames):
        rolls = RollGather().gather_by(frames)
        return sum([Score(r.to_pins()) for r in rolls], Score(0))


class BonusScoringRules:

    def __init__(self, is_bonus_frame, bonus_count):
        self.is_bonus_frame = is_bonus_frame
        self.bonus_count = bonus_count

    def calc_score(self, frames):
        self.frames = frames
        bonus_frames = [f for f in self.frames if self.is_bonus_frame(f)]
        return sum([self.calc_bonus(f) for f in bonus_frames], Score(0))

    def calc_bonus(self, frame):
        rest_rolls = self.gather_rest_rolls(frame)
        bonus_rolls = rest_rolls.take(self.bonus_count)
        return sum([Score(r.to_pins()) for r in bonus_rolls], Score(0))

    def gather_rest_rolls(self, frame):
        rest_frames = self.frames.rest(frame)
        return RollGather().gather_by(rest_frames)


class IsSpare:

    def __call__(self, frame):
        return frame.is_empty() and not frame.is_one_roll()


class IsStrike:

    def __call__(self, frame):
        return frame.is_empty() and frame.is_one_roll()


class ScoringRules:

    def __init__(self):
        self.rules = [NormalScoringRules()]
        self.rules += [BonusScoringRules(IsSpare(), 1)]
        self.rules += [BonusScoringRules(IsStrike(), 2)]

    def __iter__(self):
        for r in self.rules:
            yield r


class Score:

    def __init__(self, value):
        self.value = value

    def to_number(self):
        return self.value

    def __add__(self, rhs):
        return Score(self.value + rhs.value)


class Scorer:

    @classmethod
    def calc_score(cls, frames):
        rules = ScoringRules()
        score = sum([r.calc_score(frames) for r in rules], Score(0))
        return score.to_number()
