from DrawService import DeviceContext


class Console(DeviceContext):

    def __init__(self):
        self.clear()

    def clear(self):
        self.frame_no_line = ""
        self.pins_line = ""
        self.score_line = ""

    def draw_index(self, index):
        self.frame_no_line += "%6d" % index

    def draw_score(self, score):
        self.score_line += "%6d" % score

    def draw_pins(self, pins):
        self.pins_line += "%3s" % pins

    def draw_spare(self):
        self.pins_line += "%3s" % "/"

    def draw_strike(self):
        self.pins_line += "%3s" % "X"

    def draw_blank(self):
        self.pins_line += "%3s" % " "

    def flush(self):
        self.draw_console()
        self.clear()

    def draw_console(self):
        print(self.frame_no_line)
        print(self.pins_line)
        print(self.score_line)
