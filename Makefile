test:
	python -m unittest discover tests

clean_cache:
	rm cache/*

run_all:
	python main.py -c output.csv -a