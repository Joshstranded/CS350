# =========================================================
# Thermostat (2-button version, stable I2C, alt button logic)
# Joshua Udrea CS 350 10/19/2025
# Prof Gregori
# Button 16 = Tap = –1°F, Hold = Change Mode (OFF>HEAT>COOL)
# Button 20 = Tap = +1°F
# Red LED (18) =  Heat indicator
# Blue LED (21) = Cool indicator
# =========================================================

import time
from datetime import datetime
from threading import Thread, Lock
from gpiozero import Button, PWMLED
import board, digitalio, adafruit_ahtx0
import adafruit_character_lcd.character_lcd as characterlcd

# ------------------- GPIO SETUP -------------------
red_led = PWMLED(18)   # Heat indicator
blue_led = PWMLED(21)  # Cool indicator
button_mode = Button(16, pull_up=True, hold_time=2, bounce_time=0.3)  # Tap=–1°F, Hold=mode
button_temp = Button(20, pull_up=True, bounce_time=0.3)               # Tap=+1°F

# ------------------- LCD SETUP -------------------
lcd_rs = digitalio.DigitalInOut(board.D17)
lcd_en = digitalio.DigitalInOut(board.D27)
lcd_d4 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D23)
lcd_d6 = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)
lcd.clear()

# ------------------- SENSOR SETUP -------------------
i2c = board.I2C()
thSensor = adafruit_ahtx0.AHTx0(i2c)
i2c_lock = Lock()

# ------------------- GLOBAL STATE -------------------
modes = ["off", "heat", "cool"]
mode_index = 1     # Start in heat
setpoint = 72.0    # Default setpoint °F
running = True

# =========================================================
# Helper functions
# =========================================================

def get_temperature():
    """Thread-safe temperature read"""
    try:
        with i2c_lock:
            temp_c = thSensor.temperature
        return (temp_c * 9 / 5) + 32
    except Exception as e:
        print(f"[SENSOR ERROR] {e}")
        return None

def update_leds():
    """Update LEDs according to mode and temperature"""
    temp = get_temperature()
    if temp is None:
        red_led.off()
        blue_led.off()
        return

    if modes[mode_index] == "off":
        red_led.off()
        blue_led.off()
    elif modes[mode_index] == "heat":
        if temp < setpoint:
            red_led.pulse(fade_in_time=1, fade_out_time=1)
        else:
            red_led.value = 1
        blue_led.off()
    elif modes[mode_index] == "cool":
        if temp > setpoint:
            blue_led.pulse(fade_in_time=1, fade_out_time=1)
        else:
            blue_led.value = 1
        red_led.off()

def update_display():
    """Safely update LCD"""
    temp = get_temperature()
    now = datetime.now().strftime("%m/%d %H:%M:%S")

    if temp is None:
        line2 = "Temp: Error"
    else:
        line2 = f"T:{temp:4.1f}F  S:{setpoint:4.1f}F"

    mode_str = modes[mode_index].upper()
    lcd.message = f"{now}\n{mode_str:<5}{line2[-11:]}"

# =========================================================
# Button handlers
# =========================================================

def cycle_mode():
    """Hold on Button 16 → change mode"""
    global mode_index
    mode_index = (mode_index + 1) % len(modes)
    print(f"[MODE] {modes[mode_index].upper()}")
    update_leds()
    update_display()

def increase_temp():
    """Tap on Button 20 → increase temp"""
    global setpoint
    setpoint += 1
    print(f"[SETPOINT] ↑ {setpoint:.1f}F")
    update_leds()
    update_display()

def decrease_temp():
    """Tap on Button 16 → decrease temp"""
    global setpoint
    setpoint -= 1
    print(f"[SETPOINT] ↓ {setpoint:.1f}F")
    update_leds()
    update_display()

# =========================================================
# Attach button events
# =========================================================
button_mode.when_pressed = decrease_temp    # tap = lower temp
button_mode.when_held = cycle_mode          # hold = mode cycle
button_temp.when_pressed = increase_temp    # tap = raise temp

# =========================================================
# Background thread for LCD refresh
# =========================================================
def display_thread():
    while running:
        update_display()
        time.sleep(2)

Thread(target=display_thread, daemon=True).start()

# =========================================================
# Main loop
# =========================================================
try:
    print("[START] Thermostat running. Press Ctrl+C to exit.")
    update_leds()
    while True:
        time.sleep(0.5)

except KeyboardInterrupt:
    running = False
    lcd.clear()
    red_led.off()
    blue_led.off()
    print("\n[EXIT] Clean shutdown.")
 