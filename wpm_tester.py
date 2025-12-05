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
        
        stdscr.clear()
        result_string = (
            "You completed the test!\n"
            f"Final WPM: {wpm}\n"
            f"Final Accuracy: {accuracy}%\n\n"
            "Press 'p' to play again or any other key to exit."
        )
        stdscr.addstr(0, 0, result_string)
        stdscr.refresh()
        
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
    with open("test_sentences.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

    # return random.choice([
    #     "The quick brown fox jumps over the lazy dog.",
    #     "Never underestimate the power of a good book.",
    #     "The early bird catches the worm.",
    #     "To be or not to be, that is the question.",
    #     "The only thing we have to fear is fear itself."
    # ])


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

        if len(current_text) == len(target_text):
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
            
    total_time = max(time.time() - start_time, 1)
    final_wpm = round((len(current_text) / (total_time / 60)) / 5)

    correct_chars = 0
    for i, char in enumerate(current_text):
        if char == target_text[i]:
            correct_chars += 1
    
    accuracy = 0
    if len(target_text) > 0:
        accuracy = round((correct_chars / len(target_text)) * 100)

    return final_wpm, accuracy


wrapper(main)
