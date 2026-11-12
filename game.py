"""Game rules: pick a phrase, measure accuracy and speed. Owner: Member A.

This module only does calculations. It never opens a file and never
imports tkinter, so every function here is easy to test.
"""
import random

LEVELS = ['easy', 'medium', 'hard']


def pick_phrase(phrases, level):
    """Return the text of a random phrase of this level, or '' if there is none.

    phrases is a list of dictionaries like {'level': 'easy', 'text': 'print(1)'}.
    """
    choices = []
    for phrase in phrases:
        if phrase['level'] == level:
            choices.append(phrase['text'])
    if len(choices) == 0:
        return ''
    return random.choice(choices)


def accuracy(target, typed):
    """Return the percentage (0-100) of characters typed correctly, by position.

    Extra or missing characters count as mistakes:
    accuracy('cat', 'cat') -> 100.0, accuracy('cat', 'cut') -> 66.7
    """
    longest = max(len(target), len(typed))
    if longest == 0:
        return 0.0
    correct = 0
    for i in range(min(len(target), len(typed))):
        if target[i] == typed[i]:
            correct += 1
    return round(correct / longest * 100, 1)


def char_states(target, typed):
    """Say for every character of the target whether it is 'correct', 'wrong' or 'pending'.

    The window uses this to colour the phrase while you type:
    char_states('cat', 'cu') -> ['correct', 'wrong', 'pending']
    """
    states = []
    for i in range(len(target)):
        if i >= len(typed):
            states.append('pending')
        elif typed[i] == target[i]:
            states.append('correct')
        else:
            states.append('wrong')
    return states


def wpm(typed, seconds):
    """Return the typing speed in words per minute (1 word = 5 characters)."""
    if seconds <= 0:
        return 0.0
    words = len(typed) / 5
    minutes = seconds / 60
    return round(words / minutes, 1)


def rating(accuracy_percent, speed):
    """Turn a result into a short message for the player."""
    if accuracy_percent < 80:
        return 'Slow down and type carefully.'
    if speed >= 40:
        return 'Excellent!'
    if speed >= 25:
        return 'Good job!'
    return 'Nice and accurate. Now try a bit faster.'
