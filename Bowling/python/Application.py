from Domain import RollGather


class Archive:
    pass


class Generator:

    def __init__(self, archive, tag):
        self.archive = archive
        self.tag = tag

    def __enter__(self):
        self.archive.write_header(self.tag)

    def __exit__(self, exc_type, exc_value, traceback):
        self.archive.write_footer(self.tag)
        return True


class SaveService:

    def __init__(self, archive):
        self.archive = archive

    def save(self, game):
        with Generator(self.archive, "game"):
            frames = game.frames
            self.save_frames(frames)

    def save_frames(self, frames):
        with Generator(self.archive, "frames"):
            [self.save_frame(f) for f in frames]

    def save_frame(self, frame):
        with Generator(self.archive, "frame"):
            rolls = frame.rolls
            self.save_rolls(rolls)

    def save_rolls(self, rolls):
        with Generator(self.archive, "rolls"):
            [self.save_roll(r) for r in rolls]

    def save_roll(self, roll):
        with Generator(self.archive, "roll"):
            self.archive.write_body(roll.to_pins())


class LoadService:

    def __init__(self, archive):
        self.archive = archive
