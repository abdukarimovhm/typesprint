"""Tests for scores.py."""
import scores


def test_clean_name():
    assert scores.clean_name('  Mina ') == 'Mina'
    assert scores.clean_name('Kim, Jun') == 'Kim  Jun'


def test_save_then_load(tmp_path):
    path = str(tmp_path / 'scores.csv')
    assert scores.load_results(path) == []                  # nobody has played yet
    first = scores.make_result('Mina', 'easy', 6.24, 100.0, 38.7)
    second = scores.make_result('Jun', 'hard', 12.0, 91.5, 30.2)
    scores.save_result(path, first)
    scores.save_result(path, second)
    loaded = scores.load_results(path)
    assert len(loaded) == 2
    assert loaded[0]['name'] == 'Mina' and loaded[0]['seconds'] == 6.2
    assert loaded[1]['wpm'] == 30.2
    with open(path) as file:
        assert file.readline().strip() == scores.HEADER     # the header is written once


def test_for_player_ignores_case():
    results = [{'name': 'Mina'}, {'name': 'Jun'}, {'name': 'mina'}]
    assert len(scores.for_player(results, 'MINA')) == 2
