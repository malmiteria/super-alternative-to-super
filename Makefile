install-virtualenv:
	rm -rf local.virtualenv
	virtualenv -p python3.9 local.virtualenv
	./local.virtualenv/bin/pip install setuptools pip wheel -U
	./local.virtualenv/bin/pip install -r requirements.txt --find-links "file://${HOME}/.pip/wheelhouse"

pytest:
	./local.virtualenv/bin/pytest --cov --cov-report html --cov-report term -vv
