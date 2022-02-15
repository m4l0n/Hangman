from tkinter import *
from tkinter import messagebox
from words import word_list
import random

window_size = 700
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


class Hangman():
    def __init__(self):
        self.window = Tk()
        self.window.title('Hangman')
        self.canvas = Canvas(self.window, width=window_size, height=window_size)
        self.canvas.pack()

        self.letter_buttons = {}
        self.hangman_image = None
        self.hangman_labels = []
        self.progress = ""
        self.font = ('Nunito', '20', 'bold')
        self.refresh_image = PhotoImage(file="images/refresh.png")
        self.word = ""
        self.progress_count = 0
        self.fail_count = 0
        self.initialise_board()

    def mainloop(self):
        self.window.mainloop()

    def initialise_board(self):
        self.progress = ""
        self.word = random.choice(word_list['data'])
        self.progress_count = 0
        self.fail_count = 0

        # Letter Buttons
        for letter in letters:
            # exec('self.{} = PhotoImage(file="images/{}.png")'.format(letter, letter))
            file_path = f"images/{letter}.png"
            self.letter_buttons[letter] = PhotoImage(file=file_path)
        buttons_placement = [['b1', self.letter_buttons['a'], 18, 418], ['b2', self.letter_buttons['b'], 115, 418],
                             ['b3', self.letter_buttons['c'], 212, 418], ['b4', self.letter_buttons['d'], 309, 418],
                             ['b5', self.letter_buttons['e'], 405, 418], ['b6', self.letter_buttons['f'], 502, 418],
                             ['b7', self.letter_buttons['g'], 599, 418], ['b8', self.letter_buttons['h'], 18, 492],
                             ['b9', self.letter_buttons['i'], 115, 492], ['b10', self.letter_buttons['j'], 212, 492],
                             ['b11', self.letter_buttons['k'], 309, 492],  ['b12', self.letter_buttons['l'], 405, 492],
                             ['b13', self.letter_buttons['m'], 502, 492], ['b14', self.letter_buttons['n'], 599, 492],
                             ['b15', self.letter_buttons['o'], 18, 565], ['b16', self.letter_buttons['p'], 115, 565],
                             ['b17', self.letter_buttons['q'], 212, 565], ['b18', self.letter_buttons['r'], 309, 565],
                             ['b19', self.letter_buttons['s'], 405, 565], ['b20', self.letter_buttons['t'], 502, 565],
                             ['b21', self.letter_buttons['u'], 599, 565], ['b22', self.letter_buttons['v'], 115, 638],
                             ['b23', self.letter_buttons['w'], 212, 638], ['b24', self.letter_buttons['x'], 309, 638],
                             ['b25', self.letter_buttons['y'], 405, 638], ['b26', self.letter_buttons['z'], 502, 638]]
        # buttons_placement = [['b1', 'a', 18, 418], ['b2', 'b', 115, 418],
        #                      ['b3', 'c', 212, 418], ['b4', 'd', 309, 418],
        #                      ['b5', 'e', 405, 418], ['b6', 'f', 502, 418],
        #                      ['b7', 'g', 599, 418], ['b8', 'h', 18, 492],
        #                      ['b9', 'i', 115, 492], ['b10', 'j', 212, 492],
        #                      ['b11', 'k', 309, 492], ['b12', 'l', 405, 492],
        #                      ['b13', 'm', 502, 492], ['b14', 'n', 599, 492],
        #                      ['b15', 'o', 18, 565], ['b16', 'p', 115, 565],
        #                      ['b17', 'q', 212, 565], ['b18', 'r', 309, 565],
        #                      ['b19', 's', 405, 565], ['b20', 't', 502, 565],
        #                      ['b21', 'u', 599, 565], ['b22', 'v', 115, 638],
        #                      ['b23', 'w', 212, 638], ['b24', 'x', 309, 638],
        #                      ['b25', 'y', 405, 638], ['b26', 'z', 502, 638]]
        # Letter Buttons Placement
        for button in buttons_placement:
            # exec('{} = Button(self.window, bd=0, command=lambda:self.check("{}"), font = 10, image=self.{})'
            #      .format(button[0], button[1], button[1]))
            button[0] = Button(self.window, bd=0, command=lambda button_image=button[1]: self.check(button_image),
                               font = 10, image=button[1])
            # exec('{}.place(x={}, y={})'.format(button[0], button[2], button[3]))
            button[0].place(x=button[2], y=button[3])

        # Refresh Button
        r = Button(self.window, bd=0, font = 10, command=self.refresh_board, image=self.refresh_image)
        r.place(x=440, y=277)

        # Placing the first hangman
        self.replace_hangman(0)

        # Placing the words
        for i in range(len(self.word)):
            self.progress += "_ "
        self.place_label(self.progress)
        print(self.word)

    def check(self, button_image):
        # Get the letter associated with button_image
        letter = list(self.letter_buttons.keys())[list(self.letter_buttons.values()).index(button_image)]
        j = 0
        letter_found = False
        for i in self.word:
            if (letter == i):
                self.progress = self.progress[:j] + letter + self.progress[j+1:]
                letter_found = True
            j += 2
        if (letter_found):
            self.place_label(self.progress)
            progress_check = ''.join(self.progress.split())
            if (progress_check == self.word):
                messagebox.showinfo("Success", "You have successfully guessed the word!")
                try_again = messagebox.askyesno("Try Again?", "Do you want to try again?")
                if (try_again):
                    # Restart the game
                    self.refresh_board()
                else:
                    # Exits the program
                    self.window.destroy()
        else:
            if (self.fail_count < 10):
                self.fail_count += 1
                self.replace_hangman(self.fail_count)
            elif (self.fail_count >= 10):
                self.replace_hangman(11)
                messagebox.showerror("Fail", "You have reached the maximum tries!")
                self.refresh_board()

    # Placement of the word label on the canvas
    def place_label(self, word):
        label = Label(text=word, fg="Black", font=self.font, wraplength=216, justify="center", width=15, height=3)
        label.place(x=438, y=150)

    # Replace the hangman image
    def replace_hangman(self, i):
        file_path = f"images/hang{i}.png"
        self.hangman_image = PhotoImage(file=file_path)
        hangman_label = Label(self.window, image=self.hangman_image)
        hangman_label.place(x=20, y=87)

    def refresh_board(self):
        self.canvas.delete("all")
        self.initialise_board()


if __name__ == "__main__":
    game_instance = Hangman()
    game_instance.mainloop()