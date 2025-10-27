# Joshua Udrea CS 350 - Milestone One: PWM LED Control
# Professor Gregori

import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 18  # GPIO pin where LED is connected

# GPIO setup
GPIO.setmode(GPIO.BCM)       # Use Broadcom GPIO numbering
GPIO.setup(LED_PIN, GPIO.OUT)

# Create PWM object at 100 Hz
pwm = GPIO.PWM(LED_PIN, 100)
pwm.start(0)  # Start with LED off (0% duty cycle)

try:
    while True:
        # Fade in
        for duty in range(0, 101, 5):  # 0% to 100% in steps of 5
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.05)

        # Fade out
        for duty in range(100, -1, -5):
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    pwm.stop()
    GPIO.cleanup()
