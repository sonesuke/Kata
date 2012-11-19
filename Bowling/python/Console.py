from DrawService import DeviceContext


class Console(DeviceContext):

    def __init__(self):
        self.clear()

    def clear(self):
        self.frame_no_line = ""
        self.pins_line = ""
        self.score_line = ""

    def draw_frame_no(self, number):
        self.frame_no_line = "".join(["%6d" % (i + 1) for i in range(number)])

    def draw_pins(self, pins):
        self.pins_line += "".join(["%3s" % p for p in pins])

    def draw_score(self, score):
        self.score_line += "%6d" % score

    def flush(self):
        print(self.frame_no_line)
        print(self.pins_line)
        print(self.score_line)
        self.clear()
