run:
	python3 src/main.py

.PHONY: test
test:
	pytest -sv
