import cmd

from Model import Game, RollService
from DrawService import DrawService
from Console import Console
from SerializeService import SaveService, LoadService
from Stream import TextStream


class CUI(cmd.Cmd):

    prompt = "bowling > "

    def __init__(self):
        self.game = Game()
        super(CUI, self).__init__()

    def do_EOF(self, args):
        self.stdout.write("Exit!\n")
        return 1

    do_quit_ = do_EOF

    def do_save(self, path):
        SaveService(TextStream(open(path, 'w'))).save(self.game)

    def do_load(self, path):
        self.game = LoadService(TextStream(open(path, 'r'))).load()
        self.draw_game()

    def do_new(self, args):
        self.game = Game()
        self.draw_game()

    def do_roll(self, pins):
        RollService.roll(self.game, int(pins))
        self.draw_game()

    def draw_game(self):
        DrawService(Console()).draw(self.game)


if __name__ == '__main__':
    CUI().cmdloop()
