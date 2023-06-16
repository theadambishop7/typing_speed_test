from tkinter import *
from random import sample
import requests
import time

current_timer = None
actual_count = 0
start_time = 0

# ----------------- WORDS TO TYPE ----------------- #

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = [str(item).replace("b'", "").replace("'", "") for item in response.content.splitlines()]

current_words = []
# ----------------- TIMER ----------------- #


def count_up(count):
    global current_timer
    global actual_count
    global start_time
    if count < 10:
        count = "0" + str(count)
    timer.config(text=count)
    actual_count = time.time() - start_time
    current_timer = window.after(1000, count_up, int(count) + 1)


def start_timer():
    global current_timer
    global current_words
    global start_time
    if current_timer is not None:
        window.after_cancel(current_timer)
    start_time = time.time()
    current_timer = 0
    current_words = sample(WORDS, 20)
    text_widget.config(state=NORMAL)
    text_widget.delete("1.0", END)
    text_widget.insert(END, " ".join(current_words))
    text_widget.config(state=DISABLED)
    text_input.delete(0, END)
    count_up(0)
    text_input.focus_set()


def stop_test():
    global current_timer
    if current_timer is not None:
        window.after_cancel(current_timer)
    calculate_wpm()


def calculate_wpm():
    global current_timer
    global current_words
    global actual_count
    words_correct = 0
    user_submission = text_input.get().split()
    count_of_words_attempted = len(user_submission)
    for num in range(1, count_of_words_attempted + 1):
        if user_submission[num - 1] == current_words[num - 1]:
            words_correct += 1
    wpm = round(((words_correct * 60) / actual_count), 2)
    results_label.config(text=f"Your current WPM: {wpm}")


# ----------------- TIMER ----------------- #


window = Tk()
window.title("Typing Speed Test")
window.config(padx=100, pady=100)

title_label = Label(text="Test your typing speed!", font=("Arial", 24))
title_label.grid(row=1, column=1, columnspan=3)

text_widget = Text(window, wrap=WORD, width=40, height=5, font=("", 14), padx=5, pady=5)
text_widget.insert(END, "Insert your long text here")
text_widget.config(state=DISABLED, bd=2, relief="solid")
text_widget.grid(row=2, column=1, columnspan=3)

text_input = Entry(window, width=41)
text_input.config(bd=1)
text_input.grid(row=3, column=1, columnspan=3)

start_button = Button(text="Start Testing", command=start_timer)
start_button.grid(row=4, column=1, columnspan=1)

timer = Label(text="00", font=("Arial", 14))
timer.grid(row=4, column=2, columnspan=1)

stop_button = Button(text="Stop Testing", command=stop_test)
stop_button.grid(row=4, column=3, columnspan=1)

results_label = Label(text="")
results_label.grid(row=5, column=2, columnspan=1)


window.bind('<Return>', lambda event: stop_test())

window.mainloop()
