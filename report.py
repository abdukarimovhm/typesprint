"""Turn the saved results into reports and write them to reports/. Owner: Member D."""
import os


def leaderboard(results, top=10):
    """Return each player's BEST result, fastest first, as rows [wpm, accuracy, name].

    Only attempts with at least 80% accuracy count, so mashing keys doesn't win.
    """
    best = {}                                     # name -> [wpm, accuracy, name]
    for result in results:
        if result['accuracy'] < 80:
            continue
        name = result['name']
        row = [result['wpm'], result['accuracy'], name]
        if name not in best or row > best[name]:
            best[name] = row
    rows = sorted(best.values(), reverse=True)    # lists sort by their first item: wpm
    return rows[:top]


def player_summary(results):
    """Summarise one player's results (oldest first) in a dictionary."""
    if len(results) == 0:
        return {'attempts': 0}
    speeds = []
    accuracies = []
    for result in results:
        speeds.append(result['wpm'])
        accuracies.append(result['accuracy'])
    return {
        'attempts': len(results),
        'best_wpm': max(speeds),
        'average_wpm': round(sum(speeds) / len(speeds), 1),
        'average_accuracy': round(sum(accuracies) / len(accuracies), 1),
        'first_wpm': speeds[0],
        'last_wpm': speeds[-1],
        'improvement': round(speeds[-1] - speeds[0], 1),
    }


def leaderboard_text(rows):
    """Return the leaderboard as text, ready to show or save."""
    lines = ['TypeSprint - Leaderboard', '=' * 40,
             'Rank  Name            WPM   Accuracy']
    if len(rows) == 0:
        lines.append('No results with at least 80% accuracy yet.')
    rank = 1
    for speed, accuracy_percent, name in rows:
        lines.append(str(rank).ljust(6) + name[:15].ljust(16)
                     + str(speed).ljust(6) + str(accuracy_percent) + '%')
        rank += 1
    return '\n'.join(lines) + '\n'


def player_report_text(name, summary):
    """Return one player's report as text, ready to show or save."""
    lines = ['TypeSprint - Report for ' + name, '=' * 40]
    if summary['attempts'] == 0:
        lines.append('No attempts yet. Press Start to play!')
        return '\n'.join(lines) + '\n'
    lines.append('Attempts:          ' + str(summary['attempts']))
    lines.append('Best speed:        ' + str(summary['best_wpm']) + ' WPM')
    lines.append('Average speed:     ' + str(summary['average_wpm']) + ' WPM')
    lines.append('Average accuracy:  ' + str(summary['average_accuracy']) + '%')
    lines.append('First -> last:     ' + str(summary['first_wpm']) + ' -> '
                 + str(summary['last_wpm']) + ' WPM')
    if summary['improvement'] > 0:
        lines.append('You got ' + str(summary['improvement']) + ' WPM faster. Keep going!')
    else:
        lines.append('Practice a few more rounds to see your progress.')
    return '\n'.join(lines) + '\n'


def write_report(folder, filename, text):
    """Save the text as folder/filename (making the folder if needed). Return the path."""
    if not os.path.exists(folder):
        os.mkdir(folder)
    path = os.path.join(folder, filename)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    return path
