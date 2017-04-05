'''
* ErrorIndicator is used to alert errors via LED's
*
* Only initialization errors considered
*
* Not much can be done on an error a mile in the air
'''

import RPi.GPIO as GPIO


class ErrorIndicator:
    LEDPINS = [17, 27, 22, 18]  # [Red1, Red2, Red3, Green4]

    def __init__(self, testing):
        self.testing = testing
        if not testing:
            for pin in self.LEDPINS:
                GPIO.setup(pin, GPIO.OUT)
            GPIO.setup(23, GPIO.OUT)

    def _turn_led(self, led_num, on):  # 0 =< led_num =< 3
        if not self.testing:
            if on:
                GPIO.output(self.LEDPINS[led_num], GPIO.HIGH)
            else:
                GPIO.output(self.LEDPINS[led_num], GPIO.LOW)

    @staticmethod
    def _sound_buzzer(binary_order):  # Buzzer hot to GPIO 23
        if binary_order == [0, 0, 0, 0] or binary_order == [0, 0, 0, 1]:
            GPIO.GPIO.output(23, GPIO.LOW)
        GPIO.GPIO.output(23, GPIO.HIGH)

    def message(self, binary_order):
        self._sound_buzzer(binary_order)
        if not self.testing:
            i = 0
            for b in binary_order:
                self._turn_led(i, b)
                i += 1
        else:
            print("Error code: ", binary_order)

    def reset(self):
        self.message([0, 0, 0, 0])
