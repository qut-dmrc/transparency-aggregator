test:
	python -m unittest discover tests

system_test:
	python -m unittest discover system_tests

clean_cache:
	rm cache/*

run:
	python main.py -c output.csv -a

rund:
	python main.py -c output.csv -a --verbose
