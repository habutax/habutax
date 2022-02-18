.PHONY: test

test:
	python -m unittest discover --top-level-directory ./ --start-directory ./tests/ -v
