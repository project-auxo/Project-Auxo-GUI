import Adafruit_BBIO.GPIO as GPIO


LED_PIN = "P8_10"


class BBB(object):
    def __init__(self):
        GPIO.setup(LED_PIN, GPIO.OUT)

    @staticmethod
    def change_led(value: int):
        GPIO.output(LED_PIN, value)
