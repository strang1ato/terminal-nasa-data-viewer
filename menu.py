import curses


class Menu:
    def __init__(self, buttons, stdscr):
        self.window = stdscr
        self.window.keypad(1)
        self.position = 0
        self.buttons = buttons
        self.buttons['exit'] = 'exit'
        self.key = 'DEMO_KEY'
        self.image_size = 10

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = len(self.buttons) - 1
        elif self.position >= len(self.buttons):
            self.position = 0

    def display(self):
        self.window.clear()
        while True:
            for index, button in enumerate(self.buttons.keys()):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.COLOR_CYAN
                self.window.addstr(index+1, 1, button, mode)

            key = self.window.getch()

            if key == ord('\n'):  # '\n' means enter
                if self.position == len(self.buttons) - 1:
                    break
                else:
                    list(self.buttons.values())[self.position]()
            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)
        self.window.clear()
