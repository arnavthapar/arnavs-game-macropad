import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
import busio
import adafruit_ssd1306
from time import sleep

class Game():
    def __init__(self):
        self.c_letters = []
        self.word = "catch"
        oled.fill(0)
        oled.text("A", 0, 0, 1)
        oled.show()
        self.letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        self.selected = 0
        self.done = False
        self.guess = 0
    def key(self, key, pressed):
        # A game would go here (example here is wordle)
        # This is a very basic implementation of wordle, and does not have the word checks and randomization
        if pressed and not self.done:
            # Letter Selection
            if key == KC.UP:
                oled.fill(0)
                self.selected += 1
                if self.selected > 25:
                    self.selected = 0
                oled.text(f"{''.join(self.c_letters)}{self.letters[self.selected]}", 0, 0, 1)
                oled.show()
            elif key == KC.DOWN:
                oled.fill(0)
                self.selected -= 1
                if self.selected < 0:
                    self.selected = 25
                oled.text(f"{''.join(self.c_letters)}{self.letters[self.selected]}", 0, 0, 1)
                oled.show()
            # Choose Letter
            elif key == KC.A:
                self.c_letters.append(self.letters[self.selected])
                if len(self.c_letters) == 5:
                    shown = ""
                    for idx, i in enumerate(self.c_letters):
                        if self.word[idx] == i:
                            shown += f"~{i}~"
                        elif i in self.word:
                            shown += f"|{i}|"
                        else: shown += i
                    oled.fill(0)
                    oled.text(f"{shown}", 0, 0, 1)
                    oled.show()
                    sleep(2)
                    self.guess += 1
                    if "".join(self.c_letters) == self.word:
                        oled.fill(0)
                        oled.text("You won!", 0, 0, 1)
                        oled.show()
                        self.done = True
                    elif self.guess == 6:
                        oled.fill(0)
                        oled.text("You lost.", 0, 0, 1)
                        oled.show()
                        self.done = True
                    self.c_letters = []
            elif key == KC.B:
                if len(self.c_letters) > 0:
                    self.c_letters.pop(len(self.c_letters)-1)
                    oled.fill(0)
                    oled.text(f"{"".join(self.c_letters)}{self.letters[self.selected]}", 0, 0, 1)
                    oled.show()


i2c = busio.I2C(board.GP7, board.GP6)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
keyboard = KMKKeyboard()

# Switch pins
switch_pins = [board.D4, board.D5, board.D6, board.D7, board.D8, board.D9]
#                UP        LEFT     RIGHT     DOWN        A         B
keyboard.matrix = KeysScanner(
    pins=switch_pins,
    value_when_pressed=False  # pull-ups
)

keyboard.keymap = [
    [KC.UP, KC.LEFT, KC.RIGHT, KC.DOWN, KC.A, KC.B]
]

led1 = digitalio.DigitalInOut(board.D1)
led1.direction = digitalio.Direction.OUTPUT
led1.value = True

game = Game()

keyboard.on_key_press = game.key

if __name__ == "__main__":
    keyboard.go()