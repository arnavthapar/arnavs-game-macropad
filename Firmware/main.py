import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
import busio
import adafruit_ssd1306

class Game():
    def __init__(self):
        pass
    def key(self, key, pressed):
        if pressed:
            oled.fill(0)
            oled.text(f"{key}", 0, 0, 1)
            oled.show()
        else:
            oled.fill(0)
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