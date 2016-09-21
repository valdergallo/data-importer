# Make content for developer
help:
	@echo "setup			Instal requirements"
	@echo "test			Run suit test"
	@echo "coverage		Run Coverage"
	@echo "clean			Remove trash files"
	@echo "send_package		Send Package to Pypi"
	@echo "p3		Create docker with py3"
	@echo "p2		Create docker with py2"


setup:
	pip install -r example/requirements-dev.txt

test:
	PYTHONPATH=`pwd` py.test -x

coverage:
	rm -rf htmlcov
	py.test --cov=data_importer --cov-report html

send_package:
	python setup.py register sdist upload

clean:
	find . -name '*.pyc' -delete
	rm -rf .tox
	rm -rf data_importer.egg-info
	rm -rf cover
	rm -rf README.rst
	python setup.py clean --all

py3:
	docker-compose run -d --name py3 py3

py2:
	docker-compose run -d --name py2 py2
