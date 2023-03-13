from tkinter import *
from functools import partial


class Colour:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold, with white text
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.col_frame = Frame(padx=10, pady=10)
        self.col_frame.grid()

        self.col_heading = Label(self.col_frame,
                                 text="Colour Quest",
                                 font=("Arial", "16", "bold", )
                                 )
        self.col_heading.grid(row=0)

        instructions = "In each round you will be given six different colours to choose from. Pick a colour " \
                       "and see if you can beat the computer's score!" \
                       "\n" \
                       "\n" \
                       "To begin, choose how many rounds you'd like to play..."

        self.col_instructions = Label(self.col_frame,
                                      text=instructions,
                                      wraplength=400, width=60,
                                      justify="left")
        self.col_instructions.grid(row=1)

        self.col_error = Label(self.col_frame, text="",
                               fg="#9C0000")
        self.col_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.col_frame)
        self.button_frame.grid(row=4)

        # list to set up rounds button. First item in each
        # sublist is the background colour, second item is
        # the number of rounds
        btn_color_value = [
            ["#CC0000", 3], ["#009900", 5], ["#000099", 10]
        ]

        for item in range (0, 3):
            self.rounds_button = Button(self.button_frame,
                                        fg=button_fg,
                                        bg=btn_color_value[item][0],
                                        text="{} Rounds".format(btn_color_value[item][1]),
                                        font=button_font, width=10,
                                        command=lambda i=item: self.to_play(btn_color_value[i][1])
                                        )
            self.rounds_button.grid(row=0, column=item,
                                    padx=5, pady=5)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # if users press the cross at the top, closes help and
        # releases help button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))
        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading = "Choose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame,
                                    text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )

        self.choose_heading.grid(row=0)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        self.start_over_button = Button(self.control_frame,
                                        text="Start Over",
                                        command=self.close_play)
        self.start_over_button.grid(row=0, column=2)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Temperature Converter")
    Colour()
    root.mainloop()
