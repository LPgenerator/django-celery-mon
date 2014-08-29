clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	django-admin.py test --settings=celerymon.test_settings celerymon

coverage:
	export DJANGO_SETTINGS_MODULE=celerymon.test_settings && \
	coverage run --branch --source=celerymon `which django-admin.py` test celerymon && \
	coverage report --omit="celerymon/test*"

pep8:
	flake8 celerymon

release: clean
	python setup.py register sdist upload --sign
	python setup.py bdist_wheel upload --sign

sphinx:
	cd docs && sphinx-build -b html -d .build/doctrees . .build/html

sdist: clean
	python setup.py sdist
	ls -l dist
