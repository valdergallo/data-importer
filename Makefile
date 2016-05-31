# Make content for developer
help:
	@echo "setup			Instal requirements"
	@echo "test			Run suit test"
	@echo "coverage		Run Coverage"
	@echo "clean			Remove trash files"
	@echo "send_package		Send Package to Pypi"


setup:
	pip install -r example/requirements-dev.txt

test:
	PYTHONPATH=`pwd` py.test

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

