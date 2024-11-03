# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:26:46 2024

@author: Ezekiel
"""

import tkinter as tk #This is for GUIs
from tkinter import ttk #This is for widgets for tkinter
import random #This is used for the random numbers
from PIL import Image, ImageTk, ImageSequence  #This is used to import handling animated GIFs

class ArithmeticQuiz:
    def __init__(self, root): #Defines the class
        self.root = root 
        self.root.title("Arithmetic Quiz") #Sets window's title
        self.root.geometry("600x400")  #Sets window size
        self.root.configure(bg="#F2D5DD")  #Sets the main window background color
        self.score = 0 #This is used to track score
        self.attempts = 0 #This is used to track the number of attempts
        self.question_num = 0 #This is the questions number
        self.difficulty = 1 #This is responsible for defficulty level
        self.num1 = 0 #This is an operand
        self.num2 = 0 #This is an operand
        self.operation = "" #Operation type
        self.answer = 0 #Responsible for the correct answer
        self.time_left = 15  #Set timer to 15 seconds for each question
        self.timer_label = None #Shows timer's label
        self.timer_running = False #Responsible for the status of the timer

        self.bg_color = "#F2D5DD"    #Sets the background color to light rose
        self.btn_color = "#EDA1B5"   #Sets the color of the buttons
        self.btn_hover_color = "#F2BAC9"  #Sets the color for hovering 
        self.text_color = "#590d22"  #Sets the color of the font
        self.button_text_color = "#A40E38"  #Sets the color of the button's text

        self.font_serif = ("Times New Roman", 14) #Sets the code to TNR
        self.font_serif_bold = ("Times New Roman", 18, "bold") #Sets the code to TNR but bold

        self.frame = tk.Frame(root, padx=20, pady=20, bg=self.bg_color) #This is for the main frame
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  #This centers the frame in the window

        self.clock_gif = Image.open("C:\\Users\\Ezekiel\\Downloads\\A1 - Advanced Programming - Ezekiel Brioso\\Exercise 1\\clock.gif")  #This is the file path of the GIF i used
        self.frames = [ImageTk.PhotoImage(frame.resize((30, 30), Image.LANCZOS)) for frame in ImageSequence.Iterator(self.clock_gif)] #It loads GIF image
        self.frame_idx = 0 #It tracks the current frame of GIF's animation

        self.style = ttk.Style() #Allows us to customize the GUI's widgets
        self.style.configure("TButton", font=self.font_serif, background=self.btn_color, foreground=self.button_text_color, padding=10) #Styling buttons
        self.style.map("TButton", background=[("active", self.btn_hover_color)]) #For the button's color when being hovered

        self.display_menu() #Displays main menu
    

    def display_menu(self): #Responsible for displaying the title, adding buttons for difficulty, and clearing the frame
        self.clear_frame()

        title = tk.Label(self.frame, text="Select Difficulty Level", font=self.font_serif_bold, bg=self.bg_color, fg=self.text_color)
        title.pack(pady=(10, 20))  

        easy_button = ttk.Button(self.frame, text="1. Easy", command=lambda: self.start_quiz(1), style="TButton")
        moderate_button = ttk.Button(self.frame, text="2. Moderate", command=lambda: self.start_quiz(2), style="TButton")
        advanced_button = ttk.Button(self.frame, text="3. Advanced", command=lambda: self.start_quiz(3), style="TButton")

        easy_button.pack(pady=10)
        moderate_button.pack(pady=10)
        advanced_button.pack(pady=10)

    def start_quiz(self, difficulty): #This sets the difficult of the quiz, responsible for score, questions numbers, and as well as the starting of the first question
        self.difficulty = difficulty
        self.score = 0
        self.question_num = 0
        self.next_question()

    def next_question(self): #This code cheks if the quiz is done and if its not it will display a new problem to the user with a new set of timer
        if self.question_num >= 10:
            self.display_results()
            return

        self.num1, self.num2 = self.random_int(self.difficulty)
        self.operation = self.decide_operation()

        self.answer = self.num1 + self.num2 if self.operation == '+' else self.num1 - self.num2
        self.question_num += 1
        self.attempts = 0
        self.time_left = 15  # Reset timer to 15 seconds for each question

        self.display_problem()
        self.start_timer()

    def display_problem(self): #This clears the frame, displays the question, answer, timer, and submit button
        self.clear_frame()

        question_label = tk.Label(self.frame, text=f"Question {self.question_num}/10", font=self.font_serif_bold, bg=self.bg_color, fg=self.text_color)
        question_label.pack(pady=(10, 10)) 

        problem_text = f"{self.num1} {self.operation} {self.num2} = ?"
        problem_label = tk.Label(self.frame, text=problem_text, font=("Times New Roman", 20), bg=self.bg_color, fg=self.text_color)
        problem_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.frame, font=self.font_serif, justify='center', width=10)
        self.answer_entry.pack(pady=10)

        timer_frame = tk.Frame(self.frame, bg=self.bg_color)
        timer_frame.pack(pady=10)
        self.timer_icon_label = tk.Label(timer_frame, image=self.frames[self.frame_idx], bg=self.bg_color)
        self.timer_icon_label.pack(side="left")
        self.timer_label = tk.Label(timer_frame, text=f"Time left: {self.time_left}s", font=self.font_serif, bg=self.bg_color, fg=self.text_color)
        self.timer_label.pack(side="left")

        submit_button = ttk.Button(self.frame, text="Submit", command=self.check_answer, style="TButton")
        submit_button.pack(pady=20)

    def start_timer(self): #This starts the timer
        self.timer_running = True
        self.update_timer()

    def update_timer(self): #This is responsible for decreasing the timer in each round and will proceed to next round if it's times up
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.update_gif_frame()  # Update the GIF frame
            self.root.after(1000, self.update_timer)  # Update timer every second
        elif self.time_left <= 0:
            self.timer_running = False
            self.show_message("Time's up! Moving to next question...", "red")
            self.root.after(1000, self.next_question)

    def update_gif_frame(self): #Responsible for GIF animation
        """Update the GIF frame for the clock icon."""
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.timer_icon_label.config(image=self.frames[self.frame_idx])

    def check_answer(self): #Checks users answer
        if not self.timer_running:
            return

        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.show_message("Please enter a valid number", "red")
            return

        if user_answer == self.answer:
            points = 10 if self.attempts == 0 else 5
            self.score += points
            self.show_message(f"Correct! You earned {points} points.", "green")
            self.timer_running = False  # Stop the timer before moving to the next question
            self.root.after(1000, self.next_question)
        else:
            self.attempts += 1
            if self.attempts < 2:
                self.show_message("Wrong answer. Try again!", "red")
            else:
                self.show_message(f"Wrong! The correct answer was {self.answer}.", "red")
                self.timer_running = False  # Stop the timer before moving to the next question
                self.root.after(1000, self.next_question)

    def display_results(self): #This shows the result
        self.clear_frame()
        
        #Displays the final score that user get
        score_label = tk.Label(self.frame, text=f"Your Final Score: {self.score}/100", font=self.font_serif_bold, bg=self.bg_color, fg=self.text_color)
        score_label.pack(pady=10)

        #Displays the rank
        rank = self.get_rank(self.score)
        rank_label = tk.Label(self.frame, text=f"Rank: {rank}", font=self.font_serif, bg=self.bg_color, fg=self.text_color)
        rank_label.pack(pady=10)

        #Displays Play Again
        play_again_label = tk.Label(self.frame, text="Do you want to play again?", font=self.font_serif_bold, bg=self.bg_color, fg=self.text_color)
        play_again_label.pack(pady=10)

        #Displays Yes or No button
        yes_button = ttk.Button(self.frame, text="Yes", command=self.display_menu, style="TButton")
        yes_button.pack(pady=10)

        no_button = ttk.Button(self.frame, text="No", command=self.root.quit, style="TButton")
        no_button.pack(pady=10)

    def show_message(self, message, color): #Displays a message in the frame with the specified text and color
        message_label = tk.Label(self.frame, text=message, font=self.font_serif, bg=self.bg_color, fg=color)
        message_label.pack(pady=5)

    def random_int(self, difficulty): #Numbers generator
        if difficulty == 1:  #For Easy Mode
            return random.randint(1, 9), random.randint(1, 9)
        elif difficulty == 2:  #For Moderate Mode
            return random.randint(10, 99), random.randint(10, 99)
        else:  #For Advanced Mode
            return random.randint(1000, 9999), random.randint(1000, 9999)

    def decide_operation(self): #Randomly picks if addition or subtraction is gonna be used
        return random.choice(['+', '-'])

    def get_rank(self, score): #Assigns rank with a message
        if score >= 90:
            return "Expert \n Outstanding performance! You're a true math whiz!"
        elif score >= 75:
            return "Pro \n Well done, Pro! Your math skills are top-notch!"
        elif score >= 50:
            return "Intermediate \n Good effort! You're getting better with each question! "
        else:
            return "Beginner \n Don't worry, everyone starts somewhere! Keep practicing!"

    def clear_frame(self):#Clear all widgets from the frame
        for widget in self.frame.winfo_children():
            widget.destroy()


if __name__ == "__main__": #Starts application loop
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()
