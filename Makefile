run:
	python3 src/main.py hello

.PHONY: test
test:
	pytest -sv
