"""Command-line interface: add, list, review, stats."""

import argparse
from datetime import date

from . import db, leitner


def cmd_add(args) -> None:
    conn = db.connect()
    if db.add_word(conn, args.dutch, args.english, date.today()):
        print(f"Added: {args.dutch} = {args.english}")
    else:
        print(f"'{args.dutch}' is already in your list.")


def cmd_list(args) -> None:
    conn = db.connect()
    words = db.all_words(conn)
    if not words:
        print("No words yet. Add one with: woordjes add <dutch> <english>")
        return
    for w in words:
        print(f"[box {w['box']}] {w['dutch']:<20} {w['english']}")


def cmd_review(args) -> None:
    conn = db.connect()
    today = date.today()
    words = db.due_words(conn, today, args.limit)
    if not words:
        print("Nothing to review today. Goed gedaan! 🎉")
        return

    right = 0
    for w in words:
        try:
            answer = input(f"{w['dutch']} = ? ")
        except (EOFError, KeyboardInterrupt):
            print("\nStopped.")
            break
        correct = leitner.is_correct(answer, w["english"])
        new_box = leitner.next_box(w["box"], correct)
        db.save_answer(conn, w["id"], new_box, leitner.next_due(new_box, today), correct)
        if correct:
            right += 1
            print("  ✓ correct")
        else:
            print(f"  ✗ answer: {w['english']}")
    print(f"\n{right} right out of {len(words)}.")


def cmd_stats(args) -> None:
    conn = db.connect()
    s = db.stats(conn, date.today())
    print(f"Words: {s['total']}   Due today: {s['due']}")
    for box in range(leitner.MIN_BOX, leitner.MAX_BOX + 1):
        print(f"  box {box}: {s['per_box'].get(box, 0)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="woordjes", description="Learn Dutch words with spaced repetition."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="add a new word")
    p.add_argument("dutch")
    p.add_argument("english", help="use ';' to allow several answers")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="show all words")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("review", help="practise the words that are due")
    p.add_argument("--limit", type=int, default=None, help="max words this session")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("stats", help="show your progress")
    p.set_defaults(func=cmd_stats)
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)
