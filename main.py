BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
from types import new_class
from matplotlib.pyplot import text
import pandas
import random

TIMER = None

# Read Data

try:
    words = pandas.read_csv("data/to_learn.csv")
except FileNotFoundError:
    original_words = pandas.read_csv("data/french_words.csv")
    word_dict = original_words.to_dict(orient="records")
else:
    word_dict = words.to_dict(orient="records")
current_card = {}

# Functions

def new_word():
    global TIMER
    global current_card
    
    current_card = random.choice(word_dict)
    french_word = current_card["French"]
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    
    TIMER = window.after(3000, flip_card)
    
def flip_card():
    window.after_cancel(TIMER)
    english_word = current_card["English"]
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title_text, fill="white", text="English")
    canvas.itemconfig(word_text, fill="white", text=english_word)
    
def is_known():
    word_dict.remove(current_card)
    data = pandas.DataFrame(word_dict)
    data.to_csv("data/to_learn.csv")
    
    new_word()

# UI Setup

window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

green_btn_img = PhotoImage(file="images/right.png")
green_btn = Button(image=green_btn_img, highlightthickness=0, command=is_known)
green_btn.grid(column=1, row=1)

red_btn_img = PhotoImage(file="images/wrong.png")
red_btn = Button(image=red_btn_img, highlightthickness=0, command=new_word)
red_btn.grid(column=0, row=1)

new_word()

window.mainloop()