"""TypeSprint: a typing speed game for IGS1931.

Run it with:  python main.py

main.py only connects the pieces: it works out where the data files are and
starts the window. All the real work happens in the other modules.
"""
import os

import gui

# Build every path from the folder this file is in, so the game works
# no matter which folder you run it from (remember the Week 11 paths slide).
FOLDER = os.path.dirname(os.path.abspath(__file__))
PHRASES_FILE = os.path.join(FOLDER, 'data', 'phrases.txt')
SCORES_FILE = os.path.join(FOLDER, 'data', 'scores.csv')
REPORTS_FOLDER = os.path.join(FOLDER, 'reports')

if __name__ == '__main__':
    gui.run(PHRASES_FILE, SCORES_FILE, REPORTS_FOLDER)
