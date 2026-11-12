# Roadmap

Planned work, roughly in order. Each item will also be opened as a GitHub issue.

## v0.2 – Better input
- [ ] Import words from a CSV file (`woordjes import words.csv`)
- [ ] Export words to CSV (backup)
- [ ] Edit and delete words (`woordjes edit`, `woordjes delete`)
- [ ] Ship a starter list of common Dutch words (`data/starter_words.csv`)

## v0.3 – Smarter practice
- [ ] Reverse direction: English → Dutch
- [ ] *de* / *het* article practice mode
- [ ] Accept small typos (e.g. one wrong letter) and show the correct spelling
- [ ] Tags / topics (food, work, travel) and review by topic

## v0.4 – Motivation
- [ ] Daily streak and history of sessions
- [ ] Coloured output in the terminal
- [ ] Simple progress chart in the terminal

## Quality
- [ ] More tests (CLI commands, edge cases)
- [ ] GitHub Actions: run tests on every push
- [ ] Type hints checked with mypy, code style with ruff
- [ ] Publish to PyPI so people can `pip install woordjes`
- [ ] Better docs: usage examples and screenshots in the README
