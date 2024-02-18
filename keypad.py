"""Module for the Keypad class."""
import tkinter as tk


class Keypad(tk.Frame):
    """Keypad objects is frame contain button with keynames in requested columns"""
    standard_font = ('monospace', 14)

    def __init__(self, parent, keynames, columns=1, **kwargs):
        """Initialize a new Keypad object
                :param keynames:  list of text in the button
                :param columns: the number of column to arrange the button
        """
        super().__init__(parent, **kwargs)
        self.keynames = keynames
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        option = {'sticky': tk.NSEW, 'padx':2, 'pady':2}
        for i in range(len(self.keynames)):
            row_index = i // columns
            col_index = i % columns
            key = tk.Button(self, text=self.keynames[i], font=self.standard_font)
            key.grid(row=row_index, column=col_index, **option)

        rows = len(self.keynames) // columns
        for row in range(rows):
            self.rowconfigure(row, weight=1)

        for col in range(columns):
            self.columnconfigure(col, weight=1)

    def bind(self, sequence, function):
        """Bind an event handler to an event sequence."""
        wid_list = self.winfo_children()
        for widget in wid_list:
            widget.bind(sequence=sequence, func=function)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        wid_list = self.winfo_children()
        for widget in wid_list:
            widget[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        wid_list = self.winfo_children()
        return wid_list[0][key]

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        self.frame.configure(cnf=cnf, **kwargs)

    @property
    def frame(self):
        """return the keypad container"""
        return super()

