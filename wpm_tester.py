import curses
from curses import wrapper
import time
import random

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True:
        start_screen(stdscr)
        wpm, accuracy = wpm_test(stdscr)
        
        stdscr.addstr(4, 0, "You completed the test!")
        stdscr.addstr(5, 0, f"Final WPM: {wpm}")
        stdscr.addstr(6, 0, f"Final Accuracy: {accuracy}%")
        stdscr.addstr(8, 0, "Press 'p' to play again or any other key to exit.")
        
        key = stdscr.getkey()
        if key.lower() != 'p':
            break


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(1, 0, target)
    stdscr.addstr(2, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(1, i, char, color)


def load_text():
    return random.choice([
        "The quick brown fox jumps over the lazy dog.",
        "Never underestimate the power of a good book.",
        "The early bird catches the worm.",
        "To be or not to be, that is the question.",
        "The only thing we have to fear is fear itself."
    ])


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
            
    correct_chars = 0
    for i, char in enumerate(current_text):
        if char == target_text[i]:
            correct_chars += 1
    accuracy = round((correct_chars / len(target_text)) * 100) if target_text else 0
    
    return wpm, accuracy


wrapper(main)
