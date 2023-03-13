from tkinter import *


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

        self.three_rounds_button = Button(self.button_frame,
                                          text="3 Rounds",
                                          bg="#CC0000",
                                          fg=button_fg,
                                          font=button_font, width=12)
        self.three_rounds_button.grid(row=0, column=0, padx=5, pady=5)

        self.five_rounds_button = Button(self.button_frame,
                                         text="5 Rounds",
                                         bg="green",
                                         fg=button_fg,
                                         font=button_font, width=12,
                                         command=self.trap_card())
        self.five_rounds_button.grid(row=0, column=1, padx=5, pady=5)

        self.ten_rounds_button = Button(self.button_frame,
                                        text="10 Rounds",
                                        bg="dark blue",
                                        fg=button_fg,
                                        font=button_font, width=12)
        self.ten_rounds_button.grid(row=0, column=2, padx=5, pady=5)

    @staticmethod
    def trap_card():
        # create a new window
        trap_window = Toplevel()

        # set the title of the window
        trap_window.title("Trap Card")

        # create a label with the message
        trap_label = Label(trap_window, text="You fool! You have activated my trap card!")
        trap_label.pack(padx=20, pady=20)


# main routine
if __name__ == "__main__":
    root = Tk()
    antigravity = 1
    root.title("Temperature Converter")
    Colour()
    root.mainloop()
