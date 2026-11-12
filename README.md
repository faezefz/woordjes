# woordjes 🇳🇱

A small command-line tool to learn Dutch vocabulary with **spaced repetition**.

I moved to the Netherlands and I'm learning Dutch. Flashcard apps felt too heavy,
so I'm building a simple tool I can use every day in the terminal.
*Woordjes* means "little words" in Dutch.

## Who is it for?

People learning Dutch (or any language) who like the terminal and want a
simple, offline, no-account way to practise words.

## How it works

Words are kept in 5 boxes (the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system)):

| Box | Review again after |
|-----|--------------------|
| 1   | same day           |
| 2   | 1 day              |
| 3   | 3 days             |
| 4   | 7 days             |
| 5   | 14 days            |

A correct answer moves a word one box up. A wrong answer sends it back to box 1.
So you practise difficult words more often and easy words less often.

## Built with

- Python 3.10+ (standard library only, no extra packages)
- SQLite for storage
- pytest for tests

## Install and run

```bash
git clone https://github.com/<your-username>/woordjes.git
cd woordjes
pip install -e .
```

## Usage

```bash
woordjes add huis house
woordjes add fiets "bicycle;bike"   # ';' allows several correct answers
woordjes list
woordjes review            # practise the words due today
woordjes review --limit 10
woordjes stats
```

Example session:

```
$ woordjes review
huis = ? house
  ✓ correct
fiets = ? car
  ✗ answer: bicycle;bike

1 right out of 2.
```

Your words are stored in `~/.woordjes/words.db`.
To use a different file, set `WOORDJES_DB=/path/to/file.db`.

## Run the tests

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

See [ROADMAP.md](ROADMAP.md). Next up: CSV import, English → Dutch mode,
and *de*/*het* practice.

## License

[MIT](LICENSE)
