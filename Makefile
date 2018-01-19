test:
	python -m unittest discover tests

clean_cache:
	rm cache/*

run:
	python main.py -c output.csv -a
