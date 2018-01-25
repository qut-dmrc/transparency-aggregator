test:
	python -m unittest discover tests

system_test:
	python -m unittest discover system_tests

clear_cache:
	rm cache/*

run:
	python main.py -c output.csv -a

rund:
	python main.py -c output.csv -a --verbose

package:
	python setup.py sdist  #source dist
	python setup.py bdist_wheel #platform wheel
