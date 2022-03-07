.PHONY: test build

test:
	python -m unittest discover --top-level-directory ./ --start-directory ./tests/ -v

build:
	python -m build
