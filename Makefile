# Make content for developer
setup:
	pip install -r example/requirements.txt

test:
	python example/manage.py test data_importer -v2

coverage:
	python example/manage.py test data_importer -v2 --with-coverage

send_package:
	python setup.py register sdist upload

clean:
	find . -name '*.pyc' -delete
	rm -rf dist
	rm -rf .tox
	rm -rf data_importer.egg-info
	rm -rf cover

