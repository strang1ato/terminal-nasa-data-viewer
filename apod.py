import curses
from menu import Menu
import requests
from image_viewer import generate_image, show_image
import webbrowser


class Apod(Menu):
    def __init__(self, stdscr):
        super(Apod, self).__init__({}, stdscr)
        url = 'https://api.nasa.gov/planetary/apod?api_key=' + self.key
        self.data = requests.get(url).json()
        self.buttons = {'Show HD image': None} if self.data['media_type'] != 'video' else {'Show video': None}
        self.buttons['exit'] = None

    def display(self):
        self.window.clear()
        if self.data['media_type'] != 'video':
            h_img, w_img, img_arr = generate_image(self.data['url'], self.image_size)
        explanation = self.data['explanation'].split()
        try:
            while True:
                self.window.addstr(1, 1, self.data['title'], curses.A_BOLD)
                y_for_line = 3  # y_for_line means y for certain line in explanation
                length_of_line = 0
                self.max_y, self.max_x = self.window.getmaxyx()
                for word in explanation:
                    if length_of_line + len(word) >= self.max_x:
                        y_for_line += 1
                        length_of_line = 0
                    self.window.addstr(y_for_line, length_of_line+1, word + ' ')
                    length_of_line += len(word) + 1
                if 'copyright' in self.data:
                    if self.data['media_type'] != 'video':
                        self.window.addstr(y_for_line+1, 1, 'Image Credits: ' + self.data['copyright'],
                                        curses.color_pair(1) | curses.A_BOLD)
                    else:
                        self.window.addstr(y_for_line+1, 1, 'Video Credits: ' + self.data['copyright'],
                                        curses.color_pair(1) | curses.A_BOLD)
                else:
                    if self.data['media_type'] != 'video':
                        self.window.addstr(y_for_line+1, 1, 'Image Credits: Public Domain',
                                        curses.color_pair(1) | curses.A_BOLD)
                    else:
                        self.window.addstr(y_for_line+1, 1, 'Video Credits: Public Domain',
                                        curses.color_pair(1) | curses.A_BOLD)
                if self.data['media_type'] != 'video':
                    show_image(h_img, w_img, img_arr, y_for_line+2, self.window)
                for index, button in enumerate(self.buttons.keys()):
                    if index == self.position:
                        mode = curses.A_REVERSE
                    else:
                        mode = curses.A_NORMAL

                    if index == len(self.buttons) - 1:
                        self.window.addstr(self.max_y-1, self.max_x-len(button)-1, button, mode)
                    else:
                        self.window.addstr(self.max_y-1, 1, button, mode)
                key = self.window.getch()
                if key == ord('\n'):   # '\n' means enter
                    if self.position == len(self.buttons) - 1:
                        break
                    else:
                        webbrowser.open(self.data['hdurl'] or self.data['url'])
                elif key == curses.KEY_UP or curses.KEY_LEFT:
                    self.navigate(-1)

                elif key == curses.KEY_DOWN or curses.KEY_RIGHT:
                    self.navigate(1)
                self.window.clear()
            self.window.clear()
        except curses.error:
            raise Exception("Your terminal windows is too small!")
