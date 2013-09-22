# Make content for developer
setup:
	pip install -r example/requirements.txt

test:
	python example/manage.py test data_importer -v2 --failfast

coverage:
	python example/manage.py test data_importer -v2 --with-coverage

send_package:
	python setup.py register sdist upload

clean:
	find . -name '*.pyc' -delete
	rm -rf dist
	rm -rf cover

