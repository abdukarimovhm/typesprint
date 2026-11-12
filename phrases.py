"""The phrase bank: load, save, add, delete and filter phrases. Owner: Member B.

data/phrases.txt has one phrase per line, as  level|text :

    easy|print('hello')
    hard|def total(nums): return sum(nums)
"""
import game


def load_phrases(path):
    """Read the phrase file and return a list of {'level': ..., 'text': ...}.

    A missing file gives an empty list instead of a crash.
    """
    phrases = []
    try:
        with open(path, encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '|' not in line:
                    continue                      # skip empty or broken lines
                parts = line.split('|', 1)
                phrases.append({'level': parts[0].strip(), 'text': parts[1].strip()})
    except FileNotFoundError:
        return []
    return phrases


def save_phrases(path, phrases):
    """Write every phrase back to the file (the old content is replaced)."""
    with open(path, 'w', encoding='utf-8') as file:
        for phrase in phrases:
            file.write(phrase['level'] + '|' + phrase['text'] + '\n')


def add_phrase(phrases, level, text):
    """Add a new phrase to the list. Return True if it was added, False if not.

    It is refused when the level is unknown, the text is empty or contains '|',
    or the same text is already in the bank.
    """
    text = text.strip()
    if level not in game.LEVELS or text == '' or '|' in text:
        return False
    for phrase in phrases:
        if phrase['text'] == text:
            return False
    phrases.append({'level': level, 'text': text})
    return True


def delete_phrase(phrases, text):
    """Remove the phrase with this text. Return True if one was removed."""
    for phrase in phrases:
        if phrase['text'] == text:
            phrases.remove(phrase)
            return True
    return False


def by_level(phrases, level):
    """Return a new list with only the phrases of this level."""
    result = []
    for phrase in phrases:
        if phrase['level'] == level:
            result.append(phrase)
    return result


def count_by_level(phrases):
    """Return how many phrases each level has, e.g. {'easy': 10, 'medium': 8, 'hard': 5}."""
    counts = {}
    for level in game.LEVELS:
        counts[level] = len(by_level(phrases, level))
    return counts
