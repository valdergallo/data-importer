# Make content for developer
help:
	@echo "dev			Instal requirements"
	@echo "test			Run suit test"
	@echo "coverage		Run Coverage"
	@echo "clean			Remove trash files"
	@echo "send_package		Send Package to Pypi"
	@echo "p3		Create docker with py3"
	@echo "p2		Create docker with py2"
	@echo "update		Update all local packages"


dev:
	pip install -r requirements.txt

update:
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
	pip freeze > requirements.txt

test:
	PYTHONPATH=`pwd` py.test -s -x --nomigrations

coverage:
	rm -rf htmlcov
	PYTHONPATH=`pwd` py.test --cov=data_importer --cov-report html

send_package:
	python setup.py build bdist_wheel bdist sdist
	twine upload dist/

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
