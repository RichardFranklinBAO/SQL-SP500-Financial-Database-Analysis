.PHONY: demo test full

demo:
	python3 src/build_database.py --demo --db outputs/demo.sqlite --overwrite

test:
	python3 -m unittest discover -s tests -v

full:
	python3 src/build_database.py --data-dir data/raw --db outputs/full.sqlite --overwrite
