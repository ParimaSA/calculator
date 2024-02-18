"""Module for the Display and HistoryDisplay class."""
import tkinter as tk
from tkinter import scrolledtext


class HistoryDisplay(tk.Frame):
    """HistoryDisplay objects is frame,
    contain with scrolled text displaying history and button manage text"""
    font = ('monospace', 10)

    def __init__(self, **kwargs):
        """Initialize new HistoryDisplay object"""
        super().__init__(**kwargs)
        self.init_components()

    def init_components(self):
        """Initialize all the widget containing in HistoryDisplay"""
        history_button = tk.Button(self, text='history', font=self.font)
        history_button.bind('<Button>', self.history_button_handler)
        self.history_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=3)
        self.history_display.configure(state='disabled')

        history_button.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def history_button_handler(self, event, *args):
        """Hide/Show the history by pack and unpack the scrolled text"""
        if event.widget['text'] == 'hide_history':
            self.history_display.pack_forget()
            event.widget.config(text='history')
        else:
            self.history_display.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            event.widget.config(text='hide_history')

    def set_history(self, text: str):
        """Set the history text to the new one.
        :param text: new history"""
        self.history_display.configure(state='normal')
        self.history_display.delete(1.0, tk.END)
        self.history_display.insert(tk.INSERT, text)
        self.history_display.configure(state='disabled')


class Display(tk.Frame):
    """Display objects is frame contain label displaying an output"""
    font = ('monospace', 25)

    def __init__(self, display_format='.7G', **kwargs):
        """Initialize new Display object with the display format."""
        super().__init__(**kwargs)
        self.format = display_format
        self.init_components()

    def init_components(self):
        """Initialize all the widget in display and pack it to the Display object."""
        self.display = tk.Label(self, text='', bg='black', fg='yellow', height=3,
                                font=self.font, anchor=tk.E, width=5)
        self.display.pack(expand=True, fill=tk.BOTH)

    def set_display(self, text: str):
        """Set the display to the text
        :param text: new display
        """
        self.display.config(text=text)

    def set_format(self, display_format: str):
        """Change kind of display format
        :param display_format: 'General Format' or 'Decimal Format'
        '"""
        if display_format == 'General Format':
            self.format = self.format[:-1] + 'G'
        else:
            self.format = self.format[:-1] + 'F'

    def set_digit_format(self, digit: int):
        """Set the digit number or decimal number of the display format
        :param digit: number of the digit
        :raise TypeError: not correct digit type
        """
        if not isinstance(digit, int):
            raise TypeError
        self.format = self.format[0] + str(digit) + self.format[-1]

    def show_error(self):
        """Change display to notify error, text color = Red"""
        self.display['fg'] = 'red'

    def show_normal(self):
        """Change display to normal form, text color = Yellow"""
        self.display['fg'] = 'yellow'
