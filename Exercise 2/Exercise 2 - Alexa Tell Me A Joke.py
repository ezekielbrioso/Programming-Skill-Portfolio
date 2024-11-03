# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:21:03 2024

@author: Ezekiel
"""

import tkinter as tk
import random

def load_jokes(file_path): #Reads jokes from the file
    with open(file_path, 'r') as f:
        jokes = f.readlines()
    return [joke.strip().split('?', 1) for joke in jokes if '?' in joke]

def show_joke(): #Selects a random joke from the file, displays it, and clears the punchline and input field
    global current_joke
    current_joke = random.choice(jokes)
    joke_setup.config(text=current_joke[0] + "?")
    punchline.config(text="")  #Clears punchline
    entry.delete(0, tk.END)  #Clears the input field

#Reveals the punchline depending on the user's input
def reveal_punchline(event=None):
    user_input = entry.get().strip().lower()
    if user_input in ["why?", "how?", "what?"]:  #If the user types "why" "what" or "how"
        punchline.config(text=current_joke[1], fg=palette["text_punchline"])
    else:
        punchline.config(text="Invalid input! Try typing 'why?' 'how ?' or 'what?'.", fg="red")

def quit_app(): #Closes the app
    root.quit()

def create_rounded_button(canvas, x1, y1, x2, y2, radius=25, **kwargs): #Responsible for buttons corner
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
              x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
              x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
              x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
              x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def rounded_button(canvas, text, command, x1, y1, x2, y2, radius=25, fill="#FFC2D1", active_fill="#FFB3C6", text_color="white"): #Creates a rounded button with text inside
    rect = create_rounded_button(canvas, x1, y1, x2, y2, radius=radius, fill=fill, outline="")
    label = canvas.create_text((x1+x2)//2, (y1+y2)//2, text=text, font=font_button, fill=text_color)
    
    #Hovering
    def on_enter(event):
        canvas.itemconfig(rect, fill=active_fill)
    
    def on_leave(event):
        canvas.itemconfig(rect, fill=fill)
    
    def on_click(event):
        command()

    canvas.tag_bind(rect, "<Enter>", on_enter)
    canvas.tag_bind(rect, "<Leave>", on_leave)
    canvas.tag_bind(rect, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Enter>", on_enter)
    canvas.tag_bind(label, "<Leave>", on_leave)
    canvas.tag_bind(label, "<Button-1>", on_click)

def create_rounded_entry(canvas, x1, y1, x2, y2, radius=25, fill="#FFC2D1"): #Rounded corners' entry field
    create_rounded_button(canvas, x1, y1, x2, y2, radius=radius, fill=fill, outline="")
    entry_widget = tk.Entry(root, font=font_button, justify="center", bd=0, highlightthickness=0)
    entry_widget.place(relx=0.5, rely=(y1 + y2) / (2 * 500), anchor="center", width=x2 - x1 - 10, height=y2 - y1 - 10)
    return entry_widget

jokes = load_jokes("C:\\Users\\Ezekiel\\Downloads\\A1 - Advanced Programming - Ezekiel Brioso\\Exercise 2\\randomJokes.txt") #Load jokes from the file
current_joke = None

root = tk.Tk() #Responsible for initializing the tkinter window
root.title("Alexa Tell Me a Joke")
root.geometry("500x500")
root.resizable(0,0)

palette = { #Color palette
    "bg": "#FFE5EC",            #Background color
    "text_setup": "#FB6F92",    #Setup text color
    "text_punchline": "#FF8FAB" #Punchline text color
}

#Fonts
font_setup = ("Helvetica", 18, "bold")
font_punchline = ("Helvetica", 16, "italic")
font_button = ("Helvetica", 12)

#Applies new background color to the root window
root.config(bg=palette["bg"])

#Canvas for rounded buttons and input box
canvas = tk.Canvas(root, bg=palette["bg"], highlightthickness=0)
canvas.pack(fill="both", expand=True)

#Joke setup label
joke_setup = tk.Label(root, text="", font=font_setup, fg=palette["text_setup"], bg=palette["bg"], wraplength=450, justify="center")
joke_setup.place(relx=0.5, rely=0.2, anchor="center")

#Punchline label
punchline = tk.Label(root, text="", font=font_punchline, fg=palette["text_punchline"], bg=palette["bg"], wraplength=450, justify="center")
punchline.place(relx=0.5, rely=0.35, anchor="center")

#Rounded Entry field for user to type "why" "what" or "how"
entry = create_rounded_entry(canvas, 120, 280, 380, 330, radius=25, fill="#FFC2D1")

#Change the entry color to light pink
entry.configure(bg="#FFC2D1")

#Create rounded "Alexa tell me a Joke" button with updated colors
rounded_button(canvas, "Alexa tell me a Joke", show_joke, 100, 380, 400, 430, fill="#FFC2D1", active_fill="#FFB3C6")

#Create rounded "Quit" button with updated colors
rounded_button(canvas, "Quit", quit_app, 100, 440, 400, 490, fill="#FFC2D1", active_fill="#FFB3C6")

#Reveal punchline when Enter is pressed
root.bind("<Return>", reveal_punchline)

#Start with a joke
show_joke()

#Run the application
root.mainloop()


