from tkinter import *
from functools import partial
import csv
import random

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

        # Variables used to work out statistics when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Initially set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user score/s and computer score/s
        # used to work out statistics

        self.user_scores = []
        self.computer_scores = []

        # get all the colours for use in game
        self.all_colours = self.get_all_colours()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading = "Choose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

        instructions = "Choose one of the colours below. When you choose " \
                       "a colour, the computer's choice and the results of " \
                       "the round will be revealed"
        self.instructions_label = Label(self.quest_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        # get colours for buttons for first row..
        self.button_colours_list = []

        # get colours buttons for first round...
        self.button_colours_list = self.get_round_colours()
        print(self.button_colours_list)  # for testing purposes only, remove when finished

        # create color buttons (in choice frame)!
        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        # list to hold references for coloured buttons
        # so they can be configured for new rounds etc
        self.choice_button_ref = []

        for item in range(0, 6):
            self.choice_button = Button(self.choice_frame,
                                        width=15,
                                        command=lambda i=item: self.to_compare(self.button_colours_list[i])
                                        )
            # add button to reference list for later configuration
            self.choice_button_ref.append(self.choice_button)
            self.choice_button.grid(row=item // 3,
                                    column=item % 3,
                                    padx=5, pady=5)

        # display computer choice (after user has chosen a colour)
        self.comp_choice_label = Label(self.quest_frame,
                                       text="Computer Choice will appear here",
                                       bg="#C0C0C0", width=51)
        self.comp_choice_label.grid(row=3, pady=10)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame)
        self.rounds_frame.grid(row=4, pady=5)

        self.rounds_results_label = Label(self.rounds_frame, text="Round 1: User: - \t Computer: - \t",
                                          width=32, bg="#FFF2CC",
                                          font=("Arial", 10),
                                          pady=5)
        self.rounds_results_label.grid(row=0, column=0, padx=5)

        self.next_button = Button(self.rounds_frame, text="Next Round",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=10, state=DISABLED)
        self.next_button.grid(row=0, column=1)

        self.new_round()

        # large label to show overall game results
        self.game_results_label = Label(self.quest_frame,
                                        text="Game Totals: User: - \t Computer: - \t",
                                        bg="#FFF2CC", padx=10, pady=10,
                                        font=("Arial", 10),
                                        width=42)
        self.game_results_label.grid(row=5, pady=5)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ['#CC6000', "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        # list to hold references for coloured buttons
        # So that the text of the start over button
        # can be easily configured when the game is over
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)

    # retrieve colours from csv file
    def get_all_colours(self):
        file = open("00_colour_list_hex_v3.csv", "r")
        var_all_colors = list(csv.reader(file, delimiter=","))
        file.close()

        # removes first entry in list
        var_all_colors.pop(0)
        return var_all_colors

    # randomly choose six colours for buttons
    def get_round_colours(self):
        round_colour_list = []
        color_scores = []

        # get six unique colours
        while len(round_colour_list) < 6:
            # choose item
            chosen_colour = random.choice(self.all_colours)
            index_chosen = self.all_colours.index(chosen_colour)

            # check score is not already in list
            if chosen_colour[1] not in color_scores:
                # add item to rounds list
                round_colour_list.append(chosen_colour)
                color_scores.append(chosen_colour[1])

                # remove item from master list
                self.all_colours.pop(index_chosen)

        return round_colour_list

    # sets up new round when 'next' button is pressed
    def new_round(self):

        # disable next button (renable it at the end
        # of the round)
        self.next_button.config(state=DISABLED)

        # empty button list so we can get new colours
        self.button_colours_list.clear()

        # get new colours for buttons
        self.button_colours_list = self.get_round_colours()

        # set button bg, fg, and text
        count = 0
        for item in self.choice_button_ref:
            item['fg'] = self.button_colours_list[count][2]
            item['bg'] = self.button_colours_list[count][0]
            item['text'] = self.button_colours_list[count][0]
            item['state'] = NORMAL

            count += 1

        # retrieve number of rounds wanted / played
        # and update heading
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = "Choose - Round {} of " \
                      "{}".format(current_round + 1, how_many)
        self.choose_heading.config(text=new_heading)

    def to_compare(self, user_choice):

        how_many = self.rounds_wanted.get()

        # Add one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)

        # deactivate colour buttons!
        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        # set up background colours...
        win_colour = "#D5E8D4"
        lose_colour = "#F8CECC"

        # retrieve user score, make it into an integer
        # and add to list for stats
        user_score_current = int(user_choice[1])
        self.user_scores.append(user_score_current)

        # remove user choice from button colours list
        to_remove = self.button_colours_list.index(user_choice)
        self.button_colours_list.pop(to_remove)

        # get computer choice and add to list for stats
        # when getting score, change it to an integer before
        # appending
        comp_choice = random.choice(self.button_colours_list)
        comp_score_current = int(comp_choice[1])

        self.computer_scores.append(comp_score_current)
        comp_announce = "The computer " \
                        "chose {}".format(comp_choice[0])

        self.comp_choice_label.config(text=comp_announce,
                                      bg=comp_choice[0],
                                      fg=comp_choice[2])

        # get colours and show results!
        if user_score_current > comp_score_current:
            round_results_bg = win_colour
        else:
            round_results_bg = lose_colour

        rounds_outcome_txt = "Round {}: User {} \t" \
                             "Computer: {}".format(current_round,
                                                   user_score_current,
                                                   comp_score_current)

        self.rounds_results_label.config(bg=round_results_bg,
                                         text=rounds_outcome_txt)

        # get total scores for user and computer...
        user_total = sum(self.user_scores)
        comp_total = sum(self.computer_scores)

        if user_total > comp_total:
            self.game_results_label.config(bg=win_colour)
            status = "You Win!"
        else:
            self.game_results_label.config(bg=lose_colour)
            status = "You Lose!"

        game_outcome_txt = "Total Score: User: {} \t" \
                           "Computer: {}".format(user_total,
                                                 comp_total)
        self.game_results_label.config(text=game_outcome_txt)

        # if the game is over, disable all buttons
        # and change text of 'next' button to either
        # 'You Win' or 'You Lose' and disable all buttons

        if current_round == how_many:
            # Change 'next' button to show overall
            # win / lose result and disable it
            self.next_button.config(state=DISABLED,
                                    text=status)

            # update start over button
            start_over_button = self.control_button_ref[2]
            start_over_button['text'] = "Play Again"
            start_over_button['bg'] = "#009900"

            # change all colour buttons background to light grey
            for item in self.choice_button_ref:
                item['bg'] = "#C0C0C0"

        else:
            # enable next round button and update heading
            self.next_button.config(state=NORMAL)

    # detects which control button was pressed and
    # invokes necessary function. Can possibly replace functions
    # with calls to classes in this section!
    def to_do(self, action):
        if action == "get help":
            self.get_help()
        elif action == "get stats":
            self.get_stats()
        else:
            self.close_play()

    def get_stats(self):
        print("You chose to get the statistics")

    def get_help(self):
        print("You chose to get help")

    # DONT USE THIS FUNCTION IN BASE AS IT KILLS ROOT
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
