PYENV_HOME=venv

install-deps:
	${PYENV_HOME}/bin/pip install -U -r requirements.txt
install-dev-deps:
	${PYENV_HOME}/bin/pip install -U -r requirements-dev.txt
test:
	${PYENV_HOME}/bin/python -m py.test -v -s tests
test-behave:
	behave behave/features --stop
cov:
	${PYENV_HOME}/bin/python -m py.test --cov=restapi_project --cov-report term-missing tests
testloop:
	while true; do make test; sleep 1; done
venv:
	virtualenv -p pypy venv
	echo "../.." > venv/site-packages/app.pth
	. venv/bin/activate
	make install-deps
	make install-dev-deps
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '.coverage' `
	rm -rf `find . -type d -name '.cache' `
	rm -rf dist
	rm -rf *.egg-info

push: test clean
	${PYENV_HOME}/bin/python setup.py sdist



.PHONY: test install-deps install-dev-deps testloop cov clean push test-behave
