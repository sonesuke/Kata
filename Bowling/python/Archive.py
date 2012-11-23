from SerializeService import Archive


class TextArchive(Archive):

    def __init__(self, stream):
        self.stream = stream

    def write_header(self, tag):
        self.stream.write(tag + '\n')

    def write_footer(self, tag):
        self.stream.write('/' + tag + '\n')

    def write_count(self, count):
        self.stream.write(str(count) + '\n')

    def write_body(self, body):
        self.stream.write(str(body) + '\n')

    def load_header(self):
        return self.stream.readline().rstrip()

    def load_footer(self):
        return self.stream.readline().strip('/').rstrip()

    def load_count(self):
        return int(self.stream.readline().rstrip())

    def load_body(self):
        return int(self.stream.readline().rstrip())

    def close(self):
        self.stream.close()
