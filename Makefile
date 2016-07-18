# Make content for developer
help:
	@echo "dev			Instal requirements"
	@echo "test			Run suit test"
	@echo "coverage		Run Coverage"
	@echo "clean			Remove trash files"
	@echo "send_package		Send Package to Pypi"
	@echo "update		Update all local packages"


dev:
	pip install -r requirements.txt

update:
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
	pip freeze > requirements.txt

test:
	PYTHONPATH=`pwd` py.test -x -s

coverage:
	rm -rf htmlcov
	PYTHONPATH=`pwd` py.test --cov=data_importer --cov-report html

send_package:
	python setup.py register sdist upload

clean:
	find . -name '*.pyc' -delete
	rm -rf .tox
	rm -rf data_importer.egg-info
	rm -rf cover
	rm -rf README.rst
	python setup.py clean --all

