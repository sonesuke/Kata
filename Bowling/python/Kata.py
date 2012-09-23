

class Roll:

    def __init__(self, value=0):
        if value < 0 or 10 < value:
            raise ValueError
        self.value = value

    @property
    def score(self):
        return Score(self.value)

    def __add__(self, rhs):
        if rhs is None:
            return Roll(self.value)
        return Roll(self.value + rhs.value)


class Rolls:

    def __init__(self, rolls=None):
        self.rolls = [] if rolls is None else rolls

    def calc_score(self):
        return sum(map(lambda x: x.score, self.rolls), Score())

    def take(self, count):
        return Rolls(self.rolls[:count])

    def add(self, roll):
        self.rolls += [roll]

    def __add__(self, rhs):
        return Rolls(self.rolls + rhs.rolls)

    def is_spare(self):
        if self.is_strike():
            return False
        return sum(map(lambda x: x.score, self.rolls[:2]), Score()).is_10()

    def is_strike(self):
        return sum(map(lambda x: x.score, self.rolls[:1]), Score()).is_10()

    def is_length_equal_to(self, length):
        return len(self.rolls) == length

    def last_roll_is_10(self):
        if self.last_roll is None:
            return False
        return self.last_roll.score.is_10()

    @property
    def last_roll(self):
        if len(self.rolls) > 0:
            return self.rolls[-1]
        return None


class Score:

    def __init__(self, value=0):
        self.value = value

    def __add__(self, rhs):
        return Score(self.value + rhs.value)

    def is_10(self):
        return self.value == 10


class Frame:

    def __init__(self):
        self.rolls = Rolls()

    def roll(self, roll):
        self.valid_10_over_in_frame(roll)
        self.rolls.add(roll)

    def valid_10_over_in_frame(self, roll):
        if self.rolls.last_roll_is_10():
            return
        roll + self.rolls.last_roll

    def accept(self, aggregator):
        aggregator.add(self.rolls)

    def is_full(self):
        if self.rolls.is_strike():
            return True
        return self.rolls.is_length_equal_to(2)

    def calc_bonus_count(self):
        if self.rolls.is_strike():
            return 2
        return 1 if self.rolls.is_spare() else 0

    def calc_bonus(self, rolls_of_after_frame):
        rolls = rolls_of_after_frame.take(self.calc_bonus_count())
        return rolls.calc_score()

    def calc_score(self, rolls_of_after_frame):
        score = self.rolls.calc_score()
        score += self.calc_bonus(rolls_of_after_frame)
        return score


class Frame10(Frame):

    def is_full(self):
        if self.rolls.is_strike() or self.rolls.is_spare():
            return self.rolls.is_length_equal_to(3)
        return self.rolls.is_length_equal_to(2)


class RollAggregator:

    def __init__(self):
        self.rolls = Rolls()

    def visit(self, frame):
        frame.accept(self)

    def add(self, rolls):
        self.rolls += rolls

    def get_results(self):
        return self.rolls


class Frames:

    def __init__(self):
        self.frames = [Frame()]

    @property
    def last_frame(self):
        return self.frames[-1]

    def create_frame(self):
        if len(self.frames) == 10:
            raise ValueError
        self.frames += [Frame10()] if len(self.frames) == 9 else [Frame()]

    def roll(self, roll):
        if self.last_frame.is_full():
            self.create_frame()
        self.last_frame.roll(roll)

    def get_after_frames(self, frame):
        return self.frames[self.frames.index(frame) + 1:]

    def rolls_of_after_frame(self, frame):
        aggregator = RollAggregator()
        map(lambda x: aggregator.visit(x), self.get_after_frames(frame))
        return aggregator.get_results()

    def calc_score(self):
        calc_score = lambda x: x.calc_score(self.rolls_of_after_frame(x))
        return sum(map(lambda x: calc_score(x), self.frames), Score())


class Game:

    def __init__(self):
        self.frames = Frames()

    def roll(self, pins):
        self.frames.roll(Roll(pins))

    def calc_score(self):
        score = self.frames.calc_score()
        return score.value
