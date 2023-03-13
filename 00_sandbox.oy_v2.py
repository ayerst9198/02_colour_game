from tkinter import *
import webbrowser

class TrapCard:

    def __init__(self, parent):
        # common format for all buttons
        # Arial size 14 bold, with white text
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.trap_frame = Frame(padx=10, pady=10)
        self.trap_frame.grid()

        self.trap_label = Label(self.trap_frame,
                                 text="You fool! You have activated my trap card!",
                                 font=("Arial", "48", "bold", )
                                 )
        self.trap_label.pack(fill=BOTH, expand=1)

        # Create a button to open a link in a web browser
        self.link_button = Button(self.trap_frame, text="Click me for a surprise",
                                  font=button_font, bg="#4C4C4C", fg=button_fg,
                                  command=self.open_link)
        self.link_button.pack(side=BOTTOM, pady=10)

        # Set up fullscreen window
        self.fullscreen = Toplevel(parent)
        self.fullscreen.attributes('-fullscreen', True)
        self.fullscreen.protocol("WM_DELETE_WINDOW", self.reopen_window)
        self.fullscreen.withdraw()
        self.fullscreen_label = Label(self.fullscreen,
                                 text="You fool! You have activated my trap card!",
                                 font=("Arial", "72", "bold", )
                                 )
        self.fullscreen_label.pack(fill=BOTH, expand=1)
        self.fullscreen_button = Button(self.fullscreen, text="Click me for a surprise",
                                  font=("Arial", "36", "bold"), bg="#4C4C4C", fg=button_fg,
                                  command=self.open_link)
        self.fullscreen_button.pack(side=BOTTOM, pady=10)

    def open_link(self):
        # Open a web link in the default browser
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def reopen_window(self):
        # Reopen fullscreen window
        self.fullscreen.deiconify()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Trap Card")
    trap = TrapCard(root)
    root.mainloop()
