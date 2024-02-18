"""Module for the CalculatorController class."""
import tkinter as tk
from tkinter import ttk, messagebox
from keypad import Keypad
from calculator_display import HistoryDisplay, Display


class Calculator(tk.Tk):
    """CalculatorController is a Calculator App using logic from the model"""

    font = ('monospace', 14)
    math_function = ['exp', 'ln', 'log', 'log2', 'sqrt']

    def __init__(self, model):
        """Initialize the Calculator"""
        super().__init__()
        self.title("Calculator")
        self.geometry('320x500')
        self.model = model
        self.history = HistoryDisplay()
        self.display = Display()
        self.format = tk.StringVar()
        self.digit_point = tk.StringVar()
        self.func = tk.StringVar()
        self.history_field = tk.StringVar()
        self.init_components()

    def init_components(self):
        """Init all the component in the Calculator"""
        options = {'expand': True, 'fill': tk.BOTH}

        self.format_frame = tk.Frame(self)
        format_box = ttk.Combobox(self.format_frame, textvariable=self.format, state='readonly')
        format_box['values'] = ['General Format', 'Decimal Format']
        format_box.current(0)
        format_box.bind('<<ComboboxSelected>>', self.format_handler)
        format_label = tk.Label(self.format_frame, text='digit point: ')
        self.digit_field = tk.Entry(self.format_frame, textvariable=self.digit_point, width=1)

        self.history_box = ttk.Combobox(self, textvariable=self.history_field)
        self.history_box['values'] = ['']
        self.history_box.set('Select History')
        self.history_box.bind('<<ComboboxSelected>>', self.history_handler)
        self.history_box['state'] = 'readonly'

        math_frame = tk.Frame(self)
        math_label = tk.Label(math_frame, text='Math Function', anchor=tk.W)
        math_func = ttk.Combobox(math_frame, textvariable=self.func, state='readonly')
        math_func['values'] = self.math_function
        math_func.set('function')
        math_func.bind('<<ComboboxSelected>>', self.math_function_handler)

        line1 = tk.Frame(self)
        clear_button = tk.Button(line1, text='CLR', font=self.font, width=3, command=self.clear_button_handler)
        del_button = tk.Button(line1, text='DEL', font=self.font, width=3, command=self.delete_button_handler)
        keypad_l1 = Keypad(line1, ['(', ')', 'mod'], 3)
        keypad_l1.bind('<Button>', self.button_handler)
        keypad_l1['width'] = 3
        number_keypad = Keypad(self, list('789456123 0.'), 3)
        number_keypad.bind('<Button>', self.button_handler)
        number_keypad.configure(bg='white')
        operator_pad = Keypad(self, list('+-*/^='), 1)
        operator_pad.bind('<Button>', self.button_handler)

        format_box.pack(side=tk.LEFT, **options)
        format_label.pack(side=tk.LEFT)
        self.digit_field.pack(side=tk.LEFT, **options)
        self.format_frame.pack(side=tk.TOP, fill=tk.X)

        self.history.pack(side=tk.TOP, **options)
        self.history_box.pack(side=tk.TOP, **options)

        self.display.pack(side=tk.TOP, **options)

        math_label.pack(side=tk.LEFT, **options, padx=2, pady=2)
        math_func.pack(side=tk.LEFT, **options)
        math_frame.pack(side=tk.TOP, **options)

        clear_button.pack(side=tk.LEFT, **options)
        del_button.pack(side=tk.LEFT, **options)
        keypad_l1.pack(side=tk.LEFT, **options)
        line1.pack(side=tk.TOP, **options)
        number_keypad.pack(side=tk.LEFT, **options)
        operator_pad.pack(side=tk.LEFT, **options)

    def format_handler(self, *args):
        """Change format kind of the display and history"""
        self.display.set_format(self.format.get())
        self.digit_field.focus()
        self.model.format = self.display.format

    def digit_handler(self):
        """Change the format of display and history with the request digit or decimal point."""
        if self.digit_point.get().strip() == '':
            return
        try:
            digit = int(self.digit_point.get())
            self.display.set_digit_format(digit)
            self.digit_field.configure(fg='black')
            self.model.format = self.display.format
        except TypeError:
            self.digit_field.configure(fg='red')

    def history_handler(self, *args):
        """Change display to the selected history from the combobox."""
        if self.history_field.get() == '':
            self.history_box.set('Select History')
            return
        self.model.clear_display()
        expression, result = self.history_field.get().split('=')
        result = list(result.strip())
        self.model.display += result
        self.display.set_display(self.model.get_display())
        self.history_box.set('Select History')
        self.history_box.selection_clear()

    def math_function_handler(self, event, *args):
        """Add selected math function from the combobox to the display."""
        self.model.add_math_function(self.func.get())
        self.display.set_display(self.model.get_display())
        event.widget.set('function')
        event.widget.selection_clear()

    def button_handler(self, event, *args):
        """Keypad button handler, add the text on the button to the display."""
        add_text = event.widget['text']
        if add_text == '=':
            self.calculate()
        else:
            self.model.add_input(add_text)
            self.display.set_display(self.model.get_display())

    def clear_button_handler(self, *args):
        """Clear the display"""
        self.model.clear_display()
        self.display.set_display(self.model.get_display())

    def delete_button_handler(self, *args):
        """Delete the last part of the display"""
        self.model.del_display()
        self.display.set_display(self.model.get_display())

    def calculate(self):
        """Calculate the expression in the current display and replace it with the result."""
        try:
            self.digit_handler()
            self.model.evaluate_output()
            self.display.set_display(self.model.get_display())
            self.display.show_normal()
            self.add_history()
        except SyntaxError:
            self.display.show_error()
        except TypeError:
            self.display.show_error()
        except OverflowError:
            messagebox.showerror('ERROR', 'result too large')
            self.clear_button_handler()
        except ValueError:
            messagebox.showerror('ERROR', 'math error')
            self.clear_button_handler()

    def add_history(self):
        """Add the history to the combobox for selecting in the combobox and displaying on the scrolled text"""
        self.history_box['values'] = (self.model.history[0],) + self.history_box['values']
        self.history_box.set('Select History')
        self.history.set_history(self.model.get_all_history())

    def run(self):
        """Run the Calculator"""
        self.mainloop()
