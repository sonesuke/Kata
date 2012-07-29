

class Game:
    def __init__(self):
        self.scores = []
        self.frames = []

    def roll(self, pins):
        if 10 < pins:
            raise ValueError

        if len(self.frames) == 0:
            self.frames += [[pins]]
            return

        if len(self.frames) < 10:
            if len(self.frames[-1]) < 2 and sum(self.frames[-1]) != 10:
                if 10 < sum(self.frames[-1]) + pins:
                    raise ValueError
                self.frames[-1] += [pins]
            else:
                self.frames += [[pins]]
        elif len(self.frames) == 10:
            if self.frames[-1][0] == 10 and len(self.frames[-1]) < 2:
                self.frames[-1] += [pins]
            elif 2 == len(self.frames[-1]):
                if sum(self.frames[-1]) >= 10:
                    self.frames[-1] += [pins]
                else:
                    raise ValueError
            else:
                raise ValueError

        else:
            raise ValueError

    def score(self):
        ret = 0
        for idx in range(0, len(self.frames)):
            if 0 < idx:
                if self.frames[idx - 1][0] == 10:
                    ret += sum(self.frames[idx])
                elif sum(self.frames[idx - 1]) == 10:
                    ret += self.frames[idx][0]
            ret += sum(self.frames[idx])
            if 9 == idx:
                if self.frames[idx][0] == 10:
                    ret += sum(self.frames[idx][1:])
                elif sum(self.frames[idx][:1]) == 10:
                    ret += self.frames[idx][2]
        return ret

    def frame(self):
        return self.frames
