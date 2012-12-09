from Model import ScoreService, SpareRule, StrikeRule


class DeviceContext:

    def draw_index(self, index):
        raise NotImplemented

    def draw_pins(self, pins):
        raise NotImplemented

    def draw_pins(self, pins):
        raise NotImplemented

    def draw_strike(self):
        raise NotImplemented

    def draw_blank(self):
        raise NotImplemented

    def draw_spare(self):
        raise NotImplemented

    def draw_score(self, score):
        raise NotImplemented

    def flush(self):
        raise NotImplemented


class DrawService:

    def __init__(self, context):
        self.context = context

    def draw(self, game):
        self.draw_frames(game.get_frames())
        self.context.flush()

    def draw_frames(self, frames):
        self.frames = frames
        for f in frames:
            self.draw_frame(f)

    def draw_frame(self, frame):
        self.context.draw_index(frame.get_index())
        self.draw_frame_pins(frame)
        self.draw_score(self.frames, frame.get_index())

    def draw_score(self, frames, index):
        score = ScoreService.calculate_frames(frames[:index])
        self.context.draw_score(score)

    def draw_frame_pins(self, frame):
        self.draw_rolls(frame.get_rolls())

    def draw_rolls(self, rolls):
        if len(rolls) == 0: return
        if StrikeRule.is_satisfied_by(rolls[:1]):
            self.draw_strike(rolls)
        elif SpareRule.is_satisfied_by(rolls[:2]):
            self.draw_spare(rolls)
        else:
            self.draw_pins(rolls[0])
            self.draw_rolls(rolls[1:])

    def draw_strike(self, rolls):
        self.context.draw_strike()
        if (len(rolls[1:]) == 0): self.context.draw_blank()
        self.draw_rolls(rolls[1:])

    def draw_spare(self, rolls):
        self.draw_pins(rolls[0])
        self.context.draw_spare()
        self.draw_rolls(rolls[2:])

    def draw_pins(self, rolls):
        for r in rolls:
            self.context.draw_pins(r.to_pins())
