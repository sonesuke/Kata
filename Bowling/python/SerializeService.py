from Model import Game, Roll


class Archive:

    def write_header(self, tag):
        raise NotImplemented

    def write_footer(self, tag):
        raise NotImplemented

    def write_count(self, count):
        raise NotImplemented

    def write_body(self, body):
        raise NotImplemented

    def load_header(self):
        raise NotImplemented

    def load_footer(self):
        raise NotImplemented

    def load_count(self):
        raise NotImplemented

    def load_body(self):
        raise NotImplemented

    def close(self):
        raise NotImplemented


class Pack:

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
        with Pack(self.archive, "game"):
            frames = game.frames
            self.save_frames(frames)
        self.archive.close()

    def save_frames(self, frames):
        with Pack(self.archive, "frames"):
            self.archive.write_count(len(frames))
            [self.save_frame(f) for f in frames]

    def save_frame(self, frame):
        with Pack(self.archive, "frame"):
            rolls = frame.rolls
            self.save_rolls(rolls)

    def save_rolls(self, rolls):
        with Pack(self.archive, "rolls"):
            self.archive.write_count(len(rolls))
            [self.save_roll(r) for r in rolls]

    def save_roll(self, roll):
        with Pack(self.archive, "roll"):
            self.archive.write_body(roll.to_pins())


class Unpack:

    def __init__(self, archive, tag):
        self.archive = archive
        self.tag = tag

    def __enter__(self):
        if self.tag != self.archive.load_header():
            raise ValueError

    def __exit__(self, exc_type, exc_value, traceback):
        if self.tag != self.archive.load_footer():
            raise ValueError
        return True


class LoadService:

    def __init__(self, archive):
        self.archive = archive
        self.rolls = []

    def load(self):
        with Unpack(self.archive, "game"):
            self.load_frames()
        self.archive.close()
        return self.create_game()

    def load_frames(self):
        with Unpack(self.archive, "frames"):
            count = self.archive.load_count()
            [self.load_frame() for i in range(count)]

    def load_frame(self):
        with Unpack(self.archive, "frame"):
            self.load_rolls()

    def load_rolls(self):
        with Unpack(self.archive, "rolls"):
            count = self.archive.load_count()
            [self.load_roll() for i in range(count)]

    def load_roll(self):
        with Unpack(self.archive, "roll"):
            self.rolls += [self.archive.load_body()]

    def create_game(self):
        g = Game()
        [g.roll(r) for r in self.rolls]
        return g
