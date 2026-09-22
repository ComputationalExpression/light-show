"""LED Light Show.

CMPSC 100: Computational Expression, Lab 4

Three LEDs on a breadboard and one list to hold them. Every stage of the show
is written once, against the list, so the same program runs unchanged when
the list grows to six lights.

Every message this program prints is yours to word. The automated checks read
only the show log at the end, and which lights came on.

Author: TODO
"""

from machine import Pin
import time


def main():
    # One list holds every light, in wiring order: GP15, GP14, GP13. That
    # order is what makes leds[0] the light on GP15
    leds = [Pin(15, Pin.OUT), Pin(14, Pin.OUT), Pin(13, Pin.OUT)]

    print("=" * 50)
    print("LED LIGHT SHOW")
    print("=" * 50)

    # ===== Stage One: Roll Call =====

    # TODO 1: ask the user's name, save it to a variable called `name`

    # TODO 2: print a message that uses `name` and len(leds), then light each
    # LED in turn with a for loop over `leds`: led.on(), time.sleep(0.3),
    # led.off(), time.sleep(0.1)

    # ===== Stage Two: Spotlight =====

    print()

    # TODO 3: ask which light gets the spotlight (1-3), save it to a variable
    # called `choice`, and convert it to an int

    # TODO 4: keep `choice` between 1 and len(leds) with an if/elif, then save
    # leds[choice - 1] to a variable called `spotlight`. People count from 1
    # and lists count from 0
    # Print which light was chosen, then blink `spotlight` five times with a
    # for loop: on, time.sleep(0.2), off, time.sleep(0.2)

    # ===== Stage Three: Chase =====

    print()

    # TODO 5: ask how many rounds of the chase (1-10), save it to `rounds`,
    # and convert it to an int

    # TODO 6: run the chase with a for loop over range(rounds). Inside it,
    # print the round number, then a second for loop over `leds` lights each
    # one: led.on(), time.sleep(0.15), led.off()

    # ===== Stage Four: Your Own Pattern =====

    print()

    # TODO 7: ask how many steps are in the pattern (1-8), save it to `steps`,
    # and convert it to an int

    # TODO 8: set a variable called `pattern` to an empty list, then loop over
    # range(steps). On every trip: ask which light this step uses (1-3),
    # convert it to an int, and if it is between 1 and len(leds) append
    # `number - 1` to `pattern`; else print that there is no such light

    # TODO 9: print how many steps the pattern has, using len(pattern), then
    # play it with a for loop over `pattern`: on every trip, leds[index].on(),
    # time.sleep(0.3), leds[index].off(), time.sleep(0.1)

    # ===== Finale =====

    # TODO 10: turn every light on with a for loop over `leds`, time.sleep(1.0),
    # then turn every light off with a second for loop

    print()
    print("=" * 50)

    # TODO 11: print the show log, one line each, in this order:
    # "SHOW LOG: {name}", then a line of 50 "=" characters, then
    # "Lights: {len(leds)}", "Spotlight: {choice}", "Chase rounds: {rounds}",
    # and "Pattern steps: {len(pattern)}"
    # Print each value any way you like: commas, + with str(), or an f-string


if __name__ == "__main__":
    main()
