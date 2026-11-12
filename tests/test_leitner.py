from datetime import date

from woordjes import db, leitner


def test_correct_answer_moves_up():
    assert leitner.next_box(1, True) == 2


def test_box_never_goes_above_max():
    assert leitner.next_box(leitner.MAX_BOX, True) == leitner.MAX_BOX


def test_wrong_answer_goes_back_to_box_1():
    assert leitner.next_box(4, False) == 1


def test_next_due():
    assert leitner.next_due(3, date(2026, 11, 10)) == date(2026, 11, 13)


def test_answer_check_ignores_case_and_spaces():
    assert leitner.is_correct("  The House ", "the house")


def test_answer_check_allows_several_answers():
    assert leitner.is_correct("bike", "bicycle;bike")
    assert not leitner.is_correct("car", "bicycle;bike")


def test_database_roundtrip(tmp_path):
    conn = db.connect(tmp_path / "test.db")
    today = date(2026, 11, 10)
    assert db.add_word(conn, "huis", "house", today)
    assert not db.add_word(conn, "huis", "house", today)  # no duplicates

    word = db.due_words(conn, today)[0]
    db.save_answer(conn, word["id"], 2, date(2026, 11, 11), correct=True)

    assert db.due_words(conn, today) == []
    assert db.stats(conn, today) == {"total": 1, "due": 0, "per_box": {2: 1}}
