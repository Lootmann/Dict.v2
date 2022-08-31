run:
	python3 src/main.py hello

.PHONY: test
test:
	pytest -sv

.PHONY: clean
clean:
	rm ./.cache/dict/hello.json
