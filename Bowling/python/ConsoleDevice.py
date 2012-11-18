from DrawService import DeviceContext


class Console(DeviceContext):

    def draw_frame_no(self, number):
        [self.frame_no_line += "%6d" % (i + 1) for i in range(number)]

    def draw_pins(self, pins):
        raise NotImplemented

    def draw_score(self, score):
        raise NotImplemented

    def flush(self):
        raise NotImplemented
