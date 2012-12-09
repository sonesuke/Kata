

class Score:

    def __init__(self, value):
        self.value = value

    def to_number(self):
        return self.value

    def __add__(self, rhs):
        return Score(self.value + rhs.value)


class NormalScoringRule:

    @classmethod
    def calculate(cls, frames):
        return sum([cls.calculate_frame(f) for f in frames], Score(0))

    @classmethod
    def calculate_frame(cls, frame):
        return Score(sum([r.to_pins() for r in frame.get_rolls()]))


class BonusScoringRule:

    @classmethod
    def calculate(cls, frames):
        return sum([cls.calculate_frame(f, frames) for f in frames], Score(0))

    @classmethod
    def calculate_frame(cls, frame, frames):
        bonus_count = BonusRules.get_bonus_count(frame.get_rolls())
        rolls = cls.get_rest_rolls(frame, frames)
        return Score(sum([r.to_pins() for r in rolls[:bonus_count]]))

    @classmethod
    def get_rest_rolls(cls, frame, frames):
        rest_frames = [f for f in frames if f.get_index() > frame.get_index()]
        return sum([f.get_rolls() for f in rest_frames], Rolls())


class ScoreService:

    @classmethod
    def calculate(cls, game):
        return cls.calculate_frames(game.frames)

    @classmethod
    def calculate_frames(cls, frames):
        rules = [NormalScoringRule, BonusScoringRule]
        score = sum([r.calculate(frames) for r in rules], Score(0))
        return score.to_number()


class StrikeRule:

    @classmethod
    def is_satisfied_by(cls, rolls):
        return len(rolls) == 1 and RemainPins(rolls).is_refleshed()

    def get_bonus_count(self):
        return 2


class SpareRule:

    @classmethod
    def is_satisfied_by(cls, rolls):
        return len(rolls) != 1 and RemainPins(rolls).is_refleshed()

    def get_bonus_count(self):
        return 1


class BonusRules:

    rules = [StrikeRule, SpareRule]

    @classmethod
    def is_any(cls, rolls):
        return any([rule.is_satisfied_by(rolls) for rule in cls.rules])

    @classmethod
    def get_bonus_count(cls, rolls):
        satisfied_rule = [r for r in cls.rules if r.is_satisfied_by(rolls)]
        return sum([rule.get_bonus_count(rolls) for rule in satisfied_rule])


class IsFullCount:

    @classmethod
    def is_satisfied_by(cls, frame):
        if cls.is_last_frame_with_bonus(frame):
            return len(frame.get_rolls()) == 3
        return cls.is_full(frame)

    @classmethod
    def is_full(cls, frame):
        if RemainPins(frame.get_rolls()).is_refleshed(): return True
        return len(frame.get_rolls()) == 2

    @classmethod
    def is_last_frame_with_bonus(cls, frame):
        if not IsLastFrame.is_satisfied_by(frame):
            return False
        return BonusRules.is_any(frame.get_rolls())


class IsLastFrame:

    @classmethod
    def is_satisfied_by(cls, frame):
        return frame.get_index() == 10


class IsGameFull:

    @classmethod
    def is_satisfied_by(cls, frames):
        if frames.is_empty(): return False
        if not IsLastFrame.is_satisfied_by(frames.last()): return False
        return IsFullCount.is_satisfied_by(frames.last())


class RollService:

    @classmethod
    def roll(cls, game, pins):
        if IsGameFull.is_satisfied_by(game.get_frames()):
            raise ValueError
        cls.roll_to_frames(game.get_frames(), Roll(pins))

    @classmethod
    def roll_to_frames(cls, frames, roll):
        if frames.is_empty(): frames.create_next()
        cls.roll_to_frame(frames.last(), roll)
        if cls.is_full(frames.last()): frames.create_next()

    @classmethod
    def is_full(cls, frame):
        if IsLastFrame.is_satisfied_by(frame):
            return False
        return IsFullCount.is_satisfied_by(frame)

    @classmethod
    def roll_to_frame(cls, frame, roll):
        RemainPins(frame.get_rolls()).knock_down_by(roll)
        frame.append(roll)


class PinsServer:

    @classmethod
    def serve(cls):
        return 10


class RemainPins:

    def __init__(self, rolls):
        self.pins = PinsServer.serve()
        self.refleshed = False
        [self.knock_down_by(r) for r in rolls]

    def knock_down_by(self, roll):
        if roll.knock_down(self.pins) < 0:
            raise ValueError
        self.update(roll)

    def update(self, roll):
        self.pins = roll.knock_down(self.pins)
        self.reflesh_if_nessary()

    def reflesh_if_nessary(self):
        if self.pins == 0:
            self.pins = PinsServer.serve()
            self.refleshed = True

    def is_refleshed(self):
        return self.refleshed


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

    def __iter__(self):
        for r in self.rolls:
            yield r

    def __len__(self):
        return len(self.rolls)

    def __add__(self, rhs):
        return Rolls(self.rolls + rhs.rolls)

    def __getitem__(self, key):
        if isinstance(key, int): return Rolls([self.rolls[key]])
        return Rolls(self.rolls[key])


class Frame:

    def __init__(self, index):
        self.rolls = Rolls()
        self.index = index

    def get_index(self):
        return self.index

    def append(self, roll):
        self.rolls.append(roll)

    def get_rolls(self):
        return self.rolls


class Frames:

    def __init__(self):
        self.frames = []

    def is_empty(self):
        return len(self.frames) == 0

    def create_next(self):
        index = len(self.frames) + 1
        self.frames.append(Frame(index))

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

    def get_frames(self):
        return self.frames
