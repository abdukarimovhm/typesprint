"""Tests for report.py."""
import os

import report

RESULTS = [
    {'name': 'Mina', 'accuracy': 100.0, 'wpm': 30.0},
    {'name': 'Mina', 'accuracy': 95.0, 'wpm': 42.0},
    {'name': 'Jun', 'accuracy': 60.0, 'wpm': 80.0},      # too many mistakes: doesn't count
    {'name': 'Jun', 'accuracy': 90.0, 'wpm': 35.0},
]


def test_leaderboard_keeps_each_players_best():
    assert report.leaderboard(RESULTS) == [[42.0, 95.0, 'Mina'], [35.0, 90.0, 'Jun']]
    assert report.leaderboard(RESULTS, top=1) == [[42.0, 95.0, 'Mina']]


def test_player_summary():
    summary = report.player_summary(RESULTS[:2])
    assert summary['attempts'] == 2
    assert summary['best_wpm'] == 42.0
    assert summary['average_wpm'] == 36.0
    assert summary['average_accuracy'] == 97.5
    assert summary['improvement'] == 12.0
    assert report.player_summary([]) == {'attempts': 0}


def test_texts_and_write_report(tmp_path):
    text = report.leaderboard_text(report.leaderboard(RESULTS))
    assert 'Mina' in text and text.index('Mina') < text.index('Jun')
    assert 'Report for Mina' in report.player_report_text('Mina', report.player_summary(RESULTS[:2]))
    path = report.write_report(str(tmp_path / 'reports'), 'leaderboard.txt', text)
    assert os.path.exists(path)
    with open(path) as file:
        assert file.read() == text
