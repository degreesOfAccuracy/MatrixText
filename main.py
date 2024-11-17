import curses
import random
import time

special_characters = """ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ012345789Z:."=*+-<>¦ｸ"""

class Font:
    def __init__(self, file_path: str, character_height: int, character_order: str):
        with open(file_path) as ascii_art_file:
            ascii_art_lines = [line.strip("\n") for line in ascii_art_file.readlines()]
        self.characters = dict()
        for i, j in enumerate(range(0, len(ascii_art_lines), character_height)):
            self.characters[character_order[i]] = tuple(ascii_art_lines[j:j+character_height])
        
        self.character_height = character_height
        self.character_width = len(self.characters[character_order[0]][0])
        self.matrix_text = ["hello world"]
        self.scroll_rates = [0.5]

    def generate_matrix_text(self, height, width):
        if len(self.matrix_text) == width and len(self.matrix_text[0]) == height and len(self.scroll_rates) == width:
            for x in range(width):
                if random.random() < self.scroll_rates[x]:
                    self.matrix_text[x].pop(-1)
                    self.matrix_text[x].insert(0, random.choice(special_characters))
        else:
            self.matrix_text = []
            self.scroll_rates = []
            for x in range(width):
                self.matrix_text.append(random.choices(special_characters, k = height))
                self.scroll_rates.append(random.uniform(0.2, 0.6))

    def matrixify_text(self, start_y, start_x, text):
        matrixified_text = []
        for text_x, character in enumerate(text.lower()):
            matrixified_character = []
            for line_y, line in enumerate(self.characters[character]):
                matrixified_line = ""
                for line_x, char in enumerate(line):
                    if char != " ":
                        matrixified_line += self.matrix_text[start_x + self.character_width * text_x + line_x][start_y + line_y]
                    else:
                        matrixified_line += " "
                matrixified_character.append(matrixified_line)
            matrixified_text.append(matrixified_character)
        return matrixified_text
    
    def addmatrixstr(self, stdscr, start_y, start_x, text):
        for x, character in enumerate(self.matrixify_text(start_y, start_x, text)):
            for y, line in enumerate(character):
                stdscr.addstr(start_y + y, start_x + x * self.character_width, line, curses.color_pair(1))

def main(stdscr):
    curses.curs_set(False)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    font = Font("letters.txt", 7, " abcdefghijklmnopqrstuvwxyz0123456789?.")
    starting_time = time.time()

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        font.generate_matrix_text(height, width)
        if time.time() < starting_time + 10:
            font.addmatrixstr(stdscr, 0, 0, "Before we begin I have")
            font.addmatrixstr(stdscr, 8, 0, "one question...")
        else:
            font.addmatrixstr(stdscr, 0, 0, "Why so serious??")
        stdscr.refresh()
        time.sleep(0.1)

curses.wrapper(main)