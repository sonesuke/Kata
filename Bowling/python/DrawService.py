from ScoreService import Scorer, IsSpare, IsStrike


class DeviceContext:

    def draw_frame_no(self, number):
        raise NotImplemented

    def draw_pins(self, pins):
        raise NotImplemented

    def draw_score(self, score):
        raise NotImplemented

    def flush(self):
        raise NotImplemented


class DrawService:

    def __init__(self, context):
        self.context = context

    def draw(self, game):
        frames = game.frames
        self.context.draw_frame_no(len(frames))
        [self.draw_score(frames, index + 1) for index in range(len(frames))]
        [self.draw_pins(f) for f in frames]
        self.context.flush()

    def draw_score(self, frames, index):
        score = Scorer.calc_score(frames[:index])
        self.context.draw_score(score)

    def draw_pins(self, frame):
        pins = [str(r.to_pins()) for r in frame.rolls]
        if IsSpare()(frame):
            pins[1] = '/'
        if IsStrike()(frame):
            pins[0] = 'X'
            pins += ['']
        self.context.draw_pins(pins)
