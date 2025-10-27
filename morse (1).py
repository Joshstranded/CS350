#Joshua Udrea CS350 
# morse.py - Morse code blinking with LCD and Button

from gpiozero import LED, Button
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep

# -----------------------------
# GPIO Setup
# -----------------------------
red_led = LED(18)    # Dot = red
blue_led = LED(21)   # Dash = blue
button = Button(16)  # Button input

# LCD setup
lcd_rs = digitalio.DigitalInOut(board.D17)
lcd_en = digitalio.DigitalInOut(board.D27)
lcd_d4 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D23)
lcd_d6 = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows
)

lcd.clear()

# -----------------------------
# Timings
# -----------------------------
DOT_TIME = 0.5
DASH_TIME = 1.5
SYMBOL_PAUSE = 0.25
LETTER_PAUSE = 0.75
WORD_PAUSE = 3.0

# -----------------------------
# Messages
# -----------------------------
MESSAGE_1 = "SOS"
MESSAGE_2 = "OK"
current_message = MESSAGE_1

DEBUG = True

# -----------------------------
# Morse Dictionary
# -----------------------------
MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..",
    "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
}

# -----------------------------
# Helper Functions
# -----------------------------
def blink_dot():
    red_led.on()
    sleep(DOT_TIME)
    red_led.off()
    sleep(SYMBOL_PAUSE)

def blink_dash():
    blue_led.on()
    sleep(DASH_TIME)
    blue_led.off()
    sleep(SYMBOL_PAUSE)

def toggle_message():
    global current_message
    current_message = MESSAGE_2 if current_message == MESSAGE_1 else MESSAGE_1
    lcd.clear()
    lcd.message = f"Sending:\n{current_message}"
    if DEBUG:
        print(f"Message toggled to: {current_message}")

# Attach button press handler
button.when_pressed = toggle_message

# -----------------------------
# Morse Loop
# -----------------------------
def transmit_morse():
    global current_message
    while True:
        lcd.clear()
        lcd.message = f"Sending:\n{current_message}"

        for letter in current_message:
            morse = MORSE_CODE.get(letter.upper(), "")
            for symbol in morse:
                if symbol == ".":
                    blink_dot()
                elif symbol == "-":
                    blink_dash()
            sleep(LETTER_PAUSE)
        sleep(WORD_PAUSE)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    try:
        transmit_morse()
    except KeyboardInterrupt:
        lcd.clear()
        print("Exiting...")
