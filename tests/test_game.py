"""Tests for game.py. Run all tests from the project folder:  python -m pytest"""
import game

PHRASES = [
    {'level': 'easy', 'text': 'x = 1'},
    {'level': 'easy', 'text': 'y = 2'},
    {'level': 'hard', 'text': 'def f(): pass'},
]


def test_accuracy_perfect():
    assert game.accuracy('cat', 'cat') == 100.0


def test_accuracy_one_wrong_letter():
    assert game.accuracy('cat', 'cut') == 66.7


def test_accuracy_counts_missing_and_extra_letters():
    assert game.accuracy('cat', 'ca') == 66.7
    assert game.accuracy('cat', 'cats') == 75.0
    assert game.accuracy('', '') == 0.0


def test_char_states():
    assert game.char_states('cat', 'cu') == ['correct', 'wrong', 'pending']
    assert game.char_states('ab', 'abxyz') == ['correct', 'correct']
    assert game.char_states('', 'a') == []


def test_wpm():
    assert game.wpm('a' * 50, 60) == 10.0      # 50 characters = 10 words, in 1 minute
    assert game.wpm('a' * 50, 30) == 20.0
    assert game.wpm('abc', 0) == 0.0           # no crash when the time is 0


def test_pick_phrase_uses_the_level():
    assert game.pick_phrase(PHRASES, 'hard') == 'def f(): pass'
    assert game.pick_phrase(PHRASES, 'easy') in ['x = 1', 'y = 2']
    assert game.pick_phrase(PHRASES, 'medium') == ''


def test_rating():
    assert game.rating(70, 90) == 'Slow down and type carefully.'
    assert game.rating(95, 45) == 'Excellent!'
