"""Tests for phrases.py. tmp_path is a temporary folder that pytest gives each test."""
import phrases


def test_load_missing_file_gives_empty_list(tmp_path):
    assert phrases.load_phrases(str(tmp_path / 'nothing.txt')) == []


def test_save_then_load(tmp_path):
    path = str(tmp_path / 'phrases.txt')
    bank = [{'level': 'easy', 'text': "print('hi')"}, {'level': 'hard', 'text': 'a, b = b, a'}]
    phrases.save_phrases(path, bank)
    assert phrases.load_phrases(path) == bank


def test_add_phrase_checks_the_input():
    bank = []
    assert phrases.add_phrase(bank, 'easy', '  x = 1  ') is True
    assert bank == [{'level': 'easy', 'text': 'x = 1'}]
    assert phrases.add_phrase(bank, 'easy', 'x = 1') is False      # already there
    assert phrases.add_phrase(bank, 'expert', 'y = 2') is False    # unknown level
    assert phrases.add_phrase(bank, 'easy', '   ') is False        # empty
    assert phrases.add_phrase(bank, 'easy', 'a | b') is False      # | is the separator


def test_delete_and_count():
    bank = [{'level': 'easy', 'text': 'a'}, {'level': 'easy', 'text': 'b'},
            {'level': 'hard', 'text': 'c'}]
    assert phrases.delete_phrase(bank, 'b') is True
    assert phrases.delete_phrase(bank, 'zzz') is False
    assert phrases.by_level(bank, 'easy') == [{'level': 'easy', 'text': 'a'}]
    assert phrases.count_by_level(bank) == {'easy': 1, 'medium': 0, 'hard': 1}
