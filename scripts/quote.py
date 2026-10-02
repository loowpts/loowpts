#!/usr/bin/env python3
"""Renders assets/quote.svg: a new quote every day, in the same terminal style as the rest of the profile."""
import datetime, html, pathlib, textwrap

QUOTES = [
    ("Learn by breaking things. Preferably in staging.", "anonymous"),
    ("Almost everything will work again if you unplug it for a few minutes, including you.", "Anne Lamott"),
    ("Take care of your body. It's the only place you have to live.", "Jim Rohn"),
    ("Life is like riding a bicycle. To keep your balance, you must keep moving.", "Albert Einstein"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "proverb"),
    ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
    ("A journey of a thousand miles begins with a single step.", "Lao Tzu"),
    ("Fall seven times, stand up eight.", "Japanese proverb"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Stay hungry, stay foolish.", "Stewart Brand"),
    ("Don't count the days, make the days count.", "Muhammad Ali"),
    ("Rest is not idleness.", "John Lubbock"),
    ("There's no place like 127.0.0.1. Go home on time.", "anonymous"),
    ("Have you tried turning it off and on again? Works for people too.", "anonymous"),
    ("Close the laptop. The sunset doesn't have a replay button.", "anonymous"),
    ("Touch grass. It's free and has no rate limits.", "anonymous"),
    ("Coffee first. Everything else later.", "anonymous"),
    ("Sleep is a feature, not a bug.", "anonymous"),
    ("Go for a walk. The answer is usually outside.", "anonymous"),
    ("The only bad workout is the one that didn't happen.", "anonymous"),
    ("Rest when you're tired, not when you're done.", "anonymous"),
    ("Small steps every day beat big plans every year.", "anonymous"),
    ("Done for today is also done.", "anonymous"),
    ("Life happens outside the terminal.", "anonymous"),
    ("Discipline is choosing what you want most over what you want now.", "anonymous"),
    ("Drink water. Stretch. Call your mom.", "anonymous"),
    ("Your future self is watching. Make them proud.", "anonymous"),
    ("Balance is not something you find, it's something you create.", "anonymous"),
    ("Weekends are for living. Mondays can wait.", "anonymous"),
]

A, MUT, FG = "#93C5FD", "#6B7280", "#e6edf3"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def render(day: datetime.date) -> str:
    text, author = QUOTES[day.toordinal() % len(QUOTES)]
    lines = textwrap.wrap(text, 78)
    e = lambda s: html.escape(s, quote=False)
    y0, lh = 96, 24
    h = y0 + len(lines) * lh + 52
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 {h}" width="860" height="{h}" font-family="{MONO}" font-size="14">',
        '<defs><clipPath id="qc"><rect x="157" y="40" height="20" width="0">'
        '<animate attributeName="width" to="80" begin="0.3s" dur="0.6s" fill="freeze"/></rect></clipPath>',
    ]
    for i, line in enumerate(lines):
        out.append(f'<clipPath id="ql{i}"><rect x="36" y="{y0 + i * lh - 18}" height="26" width="0">'
                   f'<animate attributeName="width" to="{len(line) * 10 + 20}" begin="{1.0 + i * 0.9:.1f}s" dur="0.9s" fill="freeze"/></rect></clipPath>')
    out.append('</defs>')
    out.append(f'<rect width="860" height="{h}" rx="12" fill="#0d1117"/>'
               f'<rect x="0.5" y="0.5" width="859" height="{h - 1}" rx="12" fill="none" stroke="#30363d"/>')
    out.append(f'<text x="40" y="54"><tspan fill="{A}">bbxs@linux</tspan><tspan fill="{MUT}">:~$</tspan></text>'
               f'<g clip-path="url(#qc)"><text x="159" y="54" fill="{FG}">fortune</text></g>')
    out.append(f'<text x="820" y="54" text-anchor="end" fill="{MUT}" font-size="12">{e(day.strftime("%a %b %d"))}</text>')
    for i, line in enumerate(lines):
        out.append(f'<g clip-path="url(#ql{i})"><text x="40" y="{y0 + i * lh}" fill="{FG}" font-size="16.5">{e(line)}</text></g>')
    t = 1.0 + len(lines) * 0.9
    out.append(f'<text x="40" y="{y0 + len(lines) * lh + 8}" fill="{A}" opacity="0">-- {e(author)}'
               f'<set attributeName="opacity" to="1" begin="{t:.1f}s" fill="freeze"/></text>')
    out.append(f'<text x="836" y="{h - 12}" text-anchor="end" fill="#8b949e" font-size="13">whyitmakesense.</text></svg>')
    return "\n".join(out)


if __name__ == "__main__":
    path = pathlib.Path(__file__).resolve().parent.parent / "assets" / "quote.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(datetime.datetime.now(datetime.timezone.utc).date()), encoding="utf-8")
