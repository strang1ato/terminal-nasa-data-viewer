import curses
from menu import Menu
from apod import Apod


class MyApp:
    def __init__(self, stdscr):
        self.screen = stdscr
        curses.start_color()
        curses.curs_set(0)
        apod = Apod(self.screen)
        main_menu = Menu({'APOD': apod.display}, self.screen)
        main_menu.display()


if __name__ == '__main__':
    curses.wrapper(MyApp)
