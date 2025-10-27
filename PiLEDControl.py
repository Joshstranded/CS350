# Joshua Udrea
# CS 350 Mod 3 Prof Gregori
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

repeat = True

print("LED Control. Type 'on', 'off', 'exit' or 'quit'")

while repeat:
    try:
        command = input("Enter command: ").strip().lower()

        if command == "on":
            GPIO.output(18, True)
            print("LED is ON")
        elif command == "off":
            GPIO.output(18, False)
            print("LED is OFF")
        elif command in ("exit", "quit"):
            GPIO.output(18, False)
            GPIO.cleanup()
            print("Exiting...")
            repeat = False
        else:
            print("Unknown command, try 'on', 'off', 'exit' or 'quit'")

    except KeyboardInterrupt:
        GPIO.output(18, False)
        GPIO.cleanup()
        print("\nExiting due to Ctrl+C")
        repeat = False