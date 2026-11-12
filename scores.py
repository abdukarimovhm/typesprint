"""Save and load every attempt in data/scores.csv. Owner: Member C.

scores.csv looks like this (the first line is the header):

    name,level,seconds,accuracy,wpm,date
    Mina,easy,6.2,100.0,38.7,2026-11-26 10:15
"""
import os
import time

HEADER = 'name,level,seconds,accuracy,wpm,date'


def clean_name(name):
    """Tidy a player name: no spaces around it and no commas (they would break the CSV)."""
    return name.replace(',', ' ').strip()


def make_result(name, level, seconds, accuracy_percent, speed):
    """Bundle one attempt into a dictionary, with the current date and time."""
    return {
        'name': clean_name(name),
        'level': level,
        'seconds': round(seconds, 1),
        'accuracy': accuracy_percent,
        'wpm': speed,
        'date': time.strftime('%Y-%m-%d %H:%M'),
    }


def save_result(path, result):
    """Add one result as a new line at the end of the file.

    The first time, the file does not exist yet, so the header is written first.
    """
    is_new = not os.path.exists(path)
    with open(path, 'a', encoding='utf-8') as file:
        if is_new:
            file.write(HEADER + '\n')
        file.write(result['name'] + ',' + result['level'] + ',' + str(result['seconds']) + ','
                   + str(result['accuracy']) + ',' + str(result['wpm']) + ',' + result['date'] + '\n')


def load_results(path):
    """Read every result from the file. Numbers come back as floats.

    A missing file gives an empty list (nobody has played yet).
    """
    results = []
    try:
        with open(path, encoding='utf-8') as file:
            file.readline()                       # skip the header
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 6:
                    continue                      # skip empty or broken lines
                results.append({
                    'name': parts[0],
                    'level': parts[1],
                    'seconds': float(parts[2]),
                    'accuracy': float(parts[3]),
                    'wpm': float(parts[4]),
                    'date': parts[5],
                })
    except FileNotFoundError:
        return []
    return results


def for_player(results, name):
    """Return only this player's results (upper/lower case doesn't matter), oldest first."""
    mine = []
    for result in results:
        if result['name'].lower() == clean_name(name).lower():
            mine.append(result)
    return mine
