"""Module for the CalculatorModel class."""
import copy
from math import exp, log, log2, log10, sqrt


class CalculatorModel:
    """ class contain logics using in Calculator """
    operator = list('+-*/^')
    math_function = ['exp(', 'ln(', 'log(', 'log2(', 'sqrt(']

    def __init__(self):
        """Initialize a new CalculatorModel object"""
        self.display = []
        self.history = []
        self.decimal_state = False  # if current number already have decimal point or not
        self.first_digit_state = True  # if it is the starter of new number or not
        self.format = '.7G'  # format for display and history

    def add_input(self, add_text: str):
        """
        Add new input to current display
        :param add_text: new input adding to the display
        """
        if add_text in self.operator:
            self.add_operator(add_text)
        elif add_text == '.':
            self.add_decimal()
        else:
            self.add_number(add_text)

    def add_operator(self, operator: str):
        """
        Add new operator to the display. If the display already have an operator, replace it.
        :param operator: new operator
        """
        if self.display and self.display[-1] in self.operator:
            self.display = self.display[:-1]  # delete old operator
        self.display.append(operator)
        self.decimal_state = False  # start new number, not in decimal state
        self.first_digit_state = True

    def add_decimal(self):
        """Add decimal point to the display. If current number already have a decimal, display stay the same."""
        if not self.decimal_state:  # if already in decimal state, not add new decimal
            self.display.append('.')
            self.decimal_state = True  # change to decimal state
        self.first_digit_state = False

    def add_number(self, number):
        """
        Add new number to the display. If current number is zero, replace it ex. '02' = '2'.
        :params number: new number digit
        """
        self.display.append(number)
        if self.first_digit_state:
            if len(self.display) == 2:  # in start state but already have 1 digit = zero, remove zero
                self.display = [number]
            elif len(self.display) > 2 and self.display[-3] in self.operator:  # after operator, already have 1 digit
                self.display = self.display[:-2] + [number]
            self.first_digit_state = False  # change state to not first_digit_state
            if number == '0':  # if first digit still be zero, still be first digit
                self.first_digit_state = True

    def add_math_function(self, math_func: str) -> None:
        """
        Add math function to current display
        :param math_func: math function adding to the display
        :return: None

        if current display is an expression ending with the operator, add math function after
        if it is a number or expression not ending with the operator, cover it with math function
        """
        if self.display != [] and self.display[-1] not in self.operator + self.math_function:
            self.display.insert(0, math_func+'(')
            self.display.append(')')
        else:
            self.display.append(math_func+'(')

    def evaluate_output(self):
        """Evaluate the result of the display and replace display with result"""
        expression = self.display
        calculate = self.decode_display()
        result = eval(calculate)
        self.display = list(str(format(result, self.format)))  # store result to the display
        self.add_history(expression)  # add this equation to the history
        if '.' in self.display:
            self.decimal_state = True  # if the result have a decimal point, it is in decimal state

    def decode_display(self) -> str:
        """Change some keyword or operator from the current display to be able to evaluate"""
        decode = {'^': '**', 'mod': '%', 'ln(': 'log(', 'log(': 'log10('}
        func_and_operator = self.operator + self.math_function
        new_display = copy.copy(self.display)
        for current in enumerate(new_display):
            key, val = current
            if val in decode.keys():
                new_display[key] = decode[val]
            if key != 0 and val == '(' and new_display[key-1] not in func_and_operator:
                new_display[key] = '*' + val
            elif val == ')' and key != len(new_display)-1:
                if new_display[key+1] not in func_and_operator + [')']:
                    new_display[key] = val + '*'
        return ''.join(new_display)

    def clear_display(self):
        """Clear all the expression or number in the display"""
        self.display.clear()

    def del_display(self):
        """Delete last part in the display"""
        if not self.display:
            return
        self.display = self.display[:-1]

    def get_display(self) -> str:
        """Return the display, join all the part of the expression"""
        return ''.join(self.display)

    def get_all_history(self):
        """Join all the history in to one string and return"""
        return '\n'.join(self.history)

    def add_history(self, expression: list):
        """Add the equation of expression and result in format to the history
        :param expression: the expression having same result of current display
        """
        expression = ''.join(expression)
        self.history.insert(0, f'{expression:<25} = {format(float(self.get_display()), self.format)}')
