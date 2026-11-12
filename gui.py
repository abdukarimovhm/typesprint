"""The tkinter window. Owner: Member E.

This module only builds widgets and reacts to clicks and key presses. It never
opens a file itself: it asks phrases.py, scores.py and report.py to do that.
"""
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

import game
import phrases
import report
import scores

COLORS = {
    'bg': '#f4f6fb', 'card': '#ffffff', 'accent': '#2b59c3', 'accent_dark': '#1f4396',
    'text': '#1f2937', 'muted': '#6b7280', 'line': '#e5e7eb',
    'correct': '#15803d', 'wrong': '#dc2626', 'pending': '#9ca3af', 'wrong_bg': '#fee2e2',
}

# Filled in by run(): file paths, the phrase bank and the current round.
state = {'phrases_file': '', 'scores_file': '', 'reports_folder': '', 'phrases': [],
         'target': '', 'start': None, 'timer': None, 'fonts': {}}
# Filled in by build_window(): the widgets the handlers need to read or change.
ui = {}


# ================================================================ look and feel

def pick_font(root, names, size, weight='normal'):
    """Use the first font family from names that this computer has."""
    available = tkfont.families(root)
    for name in names:
        if name in available:
            return (name, size, weight)
    return ('Helvetica', size, weight)


def setup_style(root):
    """Colours and fonts for every ttk widget."""
    ui_font = ['Segoe UI', 'SF Pro Text', 'Helvetica Neue', 'Ubuntu', 'DejaVu Sans']
    code_font = ['Consolas', 'Menlo', 'SF Mono', 'DejaVu Sans Mono', 'Courier New']
    fonts = {
        'title': pick_font(root, ui_font, 20, 'bold'),
        'subtitle': pick_font(root, ui_font, 11),
        'normal': pick_font(root, ui_font, 11),
        'bold': pick_font(root, ui_font, 11, 'bold'),
        'big_number': pick_font(root, ui_font, 22, 'bold'),
        'small': pick_font(root, ui_font, 9),
        'code': pick_font(root, code_font, 18),
        'code_small': pick_font(root, code_font, 11),
    }
    state['fonts'] = fonts

    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background=COLORS['bg'], foreground=COLORS['text'], font=fonts['normal'])
    style.configure('Card.TFrame', background=COLORS['card'])
    style.configure('Card.TLabel', background=COLORS['card'])
    style.configure('Muted.TLabel', background=COLORS['card'], foreground=COLORS['muted'],
                    font=fonts['small'])
    style.configure('Number.TLabel', background=COLORS['card'], font=fonts['big_number'])
    style.configure('TButton', padding=(12, 6), background=COLORS['card'],
                    bordercolor=COLORS['line'])
    style.configure('Accent.TButton', background=COLORS['accent'], foreground='white',
                    font=fonts['bold'], bordercolor=COLORS['accent'])
    style.map('Accent.TButton', background=[('active', COLORS['accent_dark'])])
    style.configure('Treeview', rowheight=26, fieldbackground=COLORS['card'],
                    background=COLORS['card'])
    style.configure('Treeview.Heading', font=fonts['bold'])
    root.configure(background=COLORS['bg'])


# ================================================================ main window

def build_window(root):
    """Create every widget of the main window and remember the important ones in ui."""
    setup_style(root)
    fonts = state['fonts']
    root.title('TypeSprint - IGS1931')
    root.minsize(760, 560)

    # header bar
    header = tk.Frame(root, background=COLORS['accent'])
    header.pack(fill='x')
    tk.Label(header, text='TypeSprint', font=fonts['title'], fg='white',
             bg=COLORS['accent']).pack(side='left', padx=20, pady=12)
    tk.Label(header, text='How fast can you type Python?', font=fonts['subtitle'],
             fg='#dbe4ff', bg=COLORS['accent']).pack(side='left', pady=(18, 12))

    body = ttk.Frame(root, padding=20)
    body.pack(fill='both', expand=True)

    # player and level
    controls = ttk.Frame(body)
    controls.pack(fill='x')
    ttk.Label(controls, text='Player').pack(side='left')
    ui['name'] = ttk.Entry(controls, width=16)
    ui['name'].pack(side='left', padx=(6, 18))
    ttk.Label(controls, text='Level').pack(side='left')
    ui['level'] = ttk.Combobox(controls, values=game.LEVELS, width=8, state='readonly')
    ui['level'].set(game.LEVELS[0])
    ui['level'].pack(side='left', padx=6)
    ttk.Button(controls, text='Start  (Esc)', style='Accent.TButton',
               command=start_round).pack(side='right')

    # the phrase card: the text colours itself while you type
    card = ttk.Frame(body, style='Card.TFrame', padding=18)
    card.pack(fill='x', pady=16)
    ui['phrase'] = tk.Text(card, height=2, wrap='word', font=fonts['code'], relief='flat',
                           background=COLORS['card'], foreground=COLORS['pending'],
                           highlightthickness=0, cursor='arrow')
    ui['phrase'].pack(fill='x')
    ui['phrase'].tag_configure('correct', foreground=COLORS['correct'])
    ui['phrase'].tag_configure('wrong', foreground=COLORS['wrong'], background=COLORS['wrong_bg'])
    ui['phrase'].tag_configure('pending', foreground=COLORS['pending'])
    ui['phrase'].tag_configure('next', underline=True)
    show_phrase('Type your name, pick a level and press Start.')

    ui['typed'] = ttk.Entry(body, font=fonts['code'])
    ui['typed'].pack(fill='x')
    ui['typed'].bind('<KeyRelease>', on_key)
    ui['typed'].bind('<Return>', finish_round)
    root.bind('<Escape>', start_round)

    # four stat cards
    stats = ttk.Frame(body)
    stats.pack(fill='x', pady=16)
    for key, title in [('time', 'TIME'), ('accuracy', 'ACCURACY'), ('wpm', 'SPEED'),
                       ('best', 'YOUR BEST')]:
        box = ttk.Frame(stats, style='Card.TFrame', padding=(14, 10))
        box.pack(side='left', fill='x', expand=True, padx=4)
        ttk.Label(box, text=title, style='Muted.TLabel').pack(anchor='w')
        ui[key] = ttk.Label(box, text='-', style='Number.TLabel')
        ui[key].pack(anchor='w')

    ui['message'] = ttk.Label(body, text='', font=fonts['bold'])
    ui['message'].pack(anchor='w')

    # bottom buttons
    bottom = ttk.Frame(body)
    bottom.pack(side='bottom', fill='x')
    ttk.Button(bottom, text='Leaderboard', command=show_leaderboard).pack(side='left')
    ttk.Button(bottom, text='My report', command=show_my_report).pack(side='left', padx=8)
    ttk.Button(bottom, text='Manage phrases', command=open_phrase_manager).pack(side='left')
    ttk.Label(bottom, text='Enter = finish   ·   Esc = new phrase',
              foreground=COLORS['muted']).pack(side='right')


def show_phrase(text):
    """Put a new phrase in the phrase card, all grey."""
    box = ui['phrase']
    box.config(state='normal')
    box.delete('1.0', tk.END)
    box.insert('1.0', text)
    box.config(state='disabled')


def color_phrase(typed):
    """Colour every character of the phrase: green = right, red = wrong, grey = not yet."""
    box = ui['phrase']
    for tag in ['correct', 'wrong', 'pending', 'next']:
        box.tag_remove(tag, '1.0', tk.END)
    states = game.char_states(state['target'], typed)
    for i in range(len(states)):
        box.tag_add(states[i], '1.' + str(i), '1.' + str(i + 1))
    if len(typed) < len(states):
        box.tag_add('next', '1.' + str(len(typed)), '1.' + str(len(typed) + 1))


def set_stats(seconds, accuracy_percent, speed):
    ui['time'].config(text=str(round(seconds, 1)) + ' s')
    ui['accuracy'].config(text=str(accuracy_percent) + '%')
    ui['wpm'].config(text=str(speed) + ' wpm')


def update_best():
    """Show the player's best WPM so far (or '-' if they haven't played yet)."""
    mine = scores.for_player(scores.load_results(state['scores_file']), ui['name'].get())
    summary = report.player_summary(mine)
    if summary['attempts'] == 0:
        ui['best'].config(text='-')
    else:
        ui['best'].config(text=str(summary['best_wpm']) + ' wpm')


# ================================================================ a round

def start_round(event=None):
    """Pick a phrase for the chosen level and start the clock."""
    if scores.clean_name(ui['name'].get()) == '':
        messagebox.showwarning('TypeSprint', 'Please type your name first.')
        ui['name'].focus()
        return
    target = game.pick_phrase(state['phrases'], ui['level'].get())
    if target == '':
        messagebox.showwarning('TypeSprint', 'There are no phrases for this level yet. '
                                             'Add some in Manage phrases.')
        return
    if state['timer'] is not None:
        ui['typed'].after_cancel(state['timer'])
        state['timer'] = None
    state['target'] = target
    state['start'] = time.time()
    show_phrase(target)
    color_phrase('')
    ui['typed'].delete(0, tk.END)
    ui['typed'].focus()
    ui['message'].config(text='Go! Press Enter when you are done.', foreground=COLORS['accent'])
    set_stats(0, 0.0, 0.0)
    update_best()
    tick()


def tick():
    """Update the clock and the live speed 10 times a second while a round is running."""
    if state['start'] is None:
        return
    seconds = time.time() - state['start']
    typed = ui['typed'].get()
    set_stats(seconds, game.accuracy(state['target'], typed), game.wpm(typed, seconds))
    state['timer'] = ui['typed'].after(100, tick)


def on_key(event=None):
    if state['start'] is not None:
        color_phrase(ui['typed'].get())


def finish_round(event=None):
    """Stop the clock, score the attempt, save it and show the result."""
    if state['start'] is None:
        ui['message'].config(text='Press Start (or Esc) to get a phrase first.',
                             foreground=COLORS['muted'])
        return
    seconds = time.time() - state['start']
    state['start'] = None
    if state['timer'] is not None:
        ui['typed'].after_cancel(state['timer'])
        state['timer'] = None
    typed = ui['typed'].get()
    accuracy_percent = game.accuracy(state['target'], typed)
    speed = game.wpm(typed, seconds)
    result = scores.make_result(ui['name'].get(), ui['level'].get(),
                                seconds, accuracy_percent, speed)
    scores.save_result(state['scores_file'], result)
    color_phrase(typed)
    set_stats(result['seconds'], accuracy_percent, speed)
    update_best()
    color = COLORS['correct'] if accuracy_percent >= 80 else COLORS['wrong']
    ui['message'].config(text=game.rating(accuracy_percent, speed) + '   Press Esc for the next phrase.',
                         foreground=color)


# ================================================================ extra windows

def new_window(title, width, height):
    window = tk.Toplevel()
    window.title(title)
    window.configure(background=COLORS['bg'])
    window.geometry(str(width) + 'x' + str(height))
    return window


def show_leaderboard():
    """Make the leaderboard report, save it and show it as a table."""
    rows = report.leaderboard(scores.load_results(state['scores_file']))
    path = report.write_report(state['reports_folder'], 'leaderboard.txt',
                               report.leaderboard_text(rows))
    window = new_window('Leaderboard', 520, 400)
    ttk.Label(window, text='Leaderboard', font=state['fonts']['title']).pack(anchor='w', padx=16, pady=(14, 0))
    ttk.Label(window, text='Best result per player, at least 80% accuracy',
              foreground=COLORS['muted']).pack(anchor='w', padx=16)
    table = ttk.Treeview(window, columns=('rank', 'name', 'wpm', 'accuracy'), show='headings', height=10)
    for column, title, width in [('rank', '#', 40), ('name', 'Player', 200),
                                 ('wpm', 'WPM', 90), ('accuracy', 'Accuracy', 100)]:
        table.heading(column, text=title)
        table.column(column, width=width, anchor='w' if column == 'name' else 'center')
    table.tag_configure('first', background='#fff7d6')
    rank = 1
    for speed, accuracy_percent, name in rows:
        table.insert('', tk.END, values=(rank, name, speed, str(accuracy_percent) + '%'),
                     tags=('first',) if rank == 1 else ())
        rank += 1
    table.pack(fill='both', expand=True, padx=16, pady=10)
    ttk.Label(window, text='Saved to ' + path, foreground=COLORS['muted'],
              font=state['fonts']['small']).pack(anchor='w', padx=16, pady=(0, 12))


def draw_chart(canvas, speeds, width, height):
    """A simple bar chart of the WPM of each attempt (the last 12)."""
    speeds = speeds[-12:]
    canvas.create_text(10, 12, text='Speed per attempt (WPM)', anchor='w',
                       font=state['fonts']['bold'], fill=COLORS['text'])
    if len(speeds) == 0:
        return
    top, bottom, left = 34, height - 24, 16
    tallest = max(speeds) if max(speeds) > 0 else 1
    bar_space = (width - 2 * left) / len(speeds)
    for i in range(len(speeds)):
        bar_height = (bottom - top) * speeds[i] / tallest
        x0 = left + i * bar_space + 4
        x1 = left + (i + 1) * bar_space - 4
        color = COLORS['accent'] if i < len(speeds) - 1 else COLORS['correct']
        canvas.create_rectangle(x0, bottom - bar_height, x1, bottom, fill=color, width=0)
        canvas.create_text((x0 + x1) / 2, bottom - bar_height - 9, text=str(speeds[i]),
                           font=state['fonts']['small'], fill=COLORS['text'])
        canvas.create_text((x0 + x1) / 2, bottom + 10, text=str(i + 1),
                           font=state['fonts']['small'], fill=COLORS['muted'])


def show_my_report():
    """Make the report for the current player, save it and show it with a chart."""
    name = scores.clean_name(ui['name'].get())
    if name == '':
        messagebox.showwarning('TypeSprint', 'Please type your name first.')
        return
    mine = scores.for_player(scores.load_results(state['scores_file']), name)
    text = report.player_report_text(name, report.player_summary(mine))
    path = report.write_report(state['reports_folder'],
                               name.lower().replace(' ', '_') + '_report.txt', text)
    window = new_window('Report for ' + name, 560, 540)
    box = tk.Text(window, height=10, font=state['fonts']['code_small'], relief='flat',
                  background=COLORS['card'], padx=12, pady=10)
    box.insert('1.0', text)
    box.config(state='disabled')
    box.pack(fill='x', padx=16, pady=(16, 8))
    canvas = tk.Canvas(window, width=528, height=260, background=COLORS['card'], highlightthickness=0)
    canvas.pack(padx=16)
    speeds = []
    for result in mine:
        speeds.append(result['wpm'])
    draw_chart(canvas, speeds, 528, 260)
    ttk.Label(window, text='Saved to ' + path, foreground=COLORS['muted'],
              font=state['fonts']['small']).pack(anchor='w', padx=16, pady=8)


def open_phrase_manager():
    """A second window to add, delete and filter phrases (the data-management part)."""
    window = new_window('Manage phrases', 680, 460)

    top = ttk.Frame(window, padding=(16, 14, 16, 0))
    top.pack(fill='x')
    ttk.Label(top, text='Show').pack(side='left')
    show_level = ttk.Combobox(top, values=['all'] + game.LEVELS, width=8, state='readonly')
    show_level.set('all')
    show_level.pack(side='left', padx=6)
    info = ttk.Label(top, text='', foreground=COLORS['muted'])
    info.pack(side='right')

    table = ttk.Treeview(window, columns=('level', 'text'), show='headings', height=11)
    table.heading('level', text='Level')
    table.heading('text', text='Phrase')
    table.column('level', width=80, anchor='center')
    table.column('text', width=540)
    table.pack(fill='both', expand=True, padx=16, pady=10)

    add_row = ttk.Frame(window, padding=(16, 0, 16, 14))
    add_row.pack(fill='x')
    new_level = ttk.Combobox(add_row, values=game.LEVELS, width=8, state='readonly')
    new_level.set(game.LEVELS[0])
    new_level.pack(side='left')
    new_text = ttk.Entry(add_row)
    new_text.pack(side='left', fill='x', expand=True, padx=8)

    def refresh(event=None):
        table.delete(*table.get_children())
        shown = state['phrases']
        if show_level.get() != 'all':
            shown = phrases.by_level(state['phrases'], show_level.get())
        for phrase in shown:
            table.insert('', tk.END, values=(phrase['level'], phrase['text']))
        counts = phrases.count_by_level(state['phrases'])
        info.config(text='easy ' + str(counts['easy']) + '  ·  medium ' + str(counts['medium'])
                    + '  ·  hard ' + str(counts['hard']))

    def add(event=None):
        if phrases.add_phrase(state['phrases'], new_level.get(), new_text.get()):
            phrases.save_phrases(state['phrases_file'], state['phrases'])
            new_text.delete(0, tk.END)
            refresh()
        else:
            messagebox.showwarning('TypeSprint', 'Not added: it is empty, contains |, '
                                                 'or is already in the bank.', parent=window)

    def delete():
        for item in table.selection():
            phrases.delete_phrase(state['phrases'], table.item(item, 'values')[1])
        phrases.save_phrases(state['phrases_file'], state['phrases'])
        refresh()

    ttk.Button(add_row, text='Add', style='Accent.TButton', command=add).pack(side='left')
    ttk.Button(add_row, text='Delete selected', command=delete).pack(side='left', padx=(8, 0))
    new_text.bind('<Return>', add)
    show_level.bind('<<ComboboxSelected>>', refresh)
    refresh()


# ================================================================ start

def run(phrases_file, scores_file, reports_folder):
    """Load the phrase bank, build the window and start the tkinter event loop."""
    state['phrases_file'] = phrases_file
    state['scores_file'] = scores_file
    state['reports_folder'] = reports_folder
    state['phrases'] = phrases.load_phrases(phrases_file)
    root = tk.Tk()
    build_window(root)
    ui['name'].focus()
    root.mainloop()
