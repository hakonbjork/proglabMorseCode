from GPIOSimulator_v1 import *
import time
import keyboard
GPIO = GPIOSimulator()

T = 0.3


class Decoder():
    """
    docstring
    """
    morse_codes = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
                   '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
                   '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
                   '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
                   '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
                   '---..': '8', '----.': '9', '-----': '0'}

    def __init__(self):
        """ Sets up the project by defining key variables, and sets up pins"""
        self.current_symbol = ''
        self.current_word = ''
        self.current_setence = ''
        self.current_btn_state = 0

        # Setting up pins for later
        GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(PIN_RED_LED_0, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_RED_LED_1, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_RED_LED_2, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_BLUE_LED, GPIO.OUT, GPIO.LOW)

    def read_one_signal(self):
        # Read the next signal and return it

        # Find initial state and initial time
        state = GPIO.input(PIN_BTN)
        time_start = time.time()
        time_change = 0

        # Notice the time when state is changed
        # (button pressed or un-pressed)
        while True:
            new_state = GPIO.input(PIN_BTN)
            if (new_state != state):
                time_change = time.time()
                self.current_btn_state = new_state
                break
            time.sleep(0.1)  # How often the program will check button input

        # Time difference since last state change, or start of program runtime
        time_diff = time_change - time_start
        return time_diff

    def process_signals(self, signal):
        """ Examine the recently-read signal and call one of several methods"""
        """ Takes in a signal as a number of seconds """

        # If state after signal is 0, the button must have been pressed,
        # and the signal was a dot or a dash
        if (self.current_btn_state == 0):
            self.update_current_symbol(signal)
        # Else the signal must have been a break
        else:
            # Short break between signals, continue to next signal
            if (0 < signal < 2*T):
                return
            # Medium break, marks the end of a symbol
            elif (2 * T < signal < 9*T):
                self.handle_symbol_end()
            # Long break, marks the end of a word
            else:
                self.handle_word_end()

    def update_current_symbol(self, signal):
        """ Append the current dot or dash onto the end of current symbol """

        # Short signal, dot
        if (0 < signal < 2*T):
            self.blink_red()
            self.current_symbol += '.'

        # Long signal, dash
        else:
            self.blink_blue()
            self.current_symbol += '-'

    def handle_symbol_end(self):
        """ Finds the current letter, updates current word and """
        """ resets the current symbol """

        symbol = self.morse_codes.get(self.current_symbol)
        self.update_current_word(symbol)
        self.current_symbol = ''

    def update_current_word(self, symbol):
        """ Adds the most recently completed symbol onto current word """
        if (symbol != None):
            self.current_word += str(symbol)
        #self.current_word += str(symbol)

    def handle_word_end(self):
        """ Process to handle end of word """

        self.handle_symbol_end()

        # The 3 next lines are not nessecary for task, add to setence
        if (self.current_word != None):
            self.current_setence += self.current_word
        self.current_setence += ' '

        print('-------------------------------')
        print(self.current_word)
        print('-------------------------------')
        self.current_word = ''  # resets word

    def blink_red(self):
        """ Helper function to make red LEDs blink """
        GPIO.output(PIN_RED_LED_0, GPIO.HIGH)
        GPIO.output(PIN_RED_LED_1, GPIO.HIGH)
        GPIO.output(PIN_RED_LED_2, GPIO.HIGH)
        GPIO.output(PIN_RED_LED_0, GPIO.LOW)
        GPIO.output(PIN_RED_LED_1, GPIO.LOW)
        GPIO.output(PIN_RED_LED_2, GPIO.LOW)

    def blink_blue(self):
        """ Helper function to make blue LED blink """
        GPIO.output(PIN_BLUE_LED, GPIO.HIGH)
        GPIO.output(PIN_BLUE_LED, GPIO.LOW)


decoder = Decoder()

# while keyboard.is_pressed('q') == False:


def main():
    while keyboard.is_pressed('q') == False:
        signal = decoder.read_one_signal()
        decoder.process_signals(signal)
        # print(decoder.current_symbol)
    print('Setence: ' + str(decoder.current_setence))


main()
