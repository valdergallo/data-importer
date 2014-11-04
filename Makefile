# Make content for developer
help:
	@echo "setup			Instal requirements"
	@echo "test			Run suit test"
	@echo "coverage		Run Coverage"
	@echo "clean			Remove trash files"
	@echo "send_package		Send Package to Pypi"


setup:
	pip install -r example/requirements.txt

test:
	python example/manage.py test data_importer -v 2

coverage:
	python example/manage.py test data_importer -v 2 --with-coverage

send_package:
	python setup.py register sdist upload

clean:
	find . -name '*.pyc' -delete
	rm -rf dist
	rm -rf .tox
	rm -rf data_importer.egg-info
	rm -rf cover

