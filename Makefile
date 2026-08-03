init:
	pip install .[develop]

test:
	py.test tests/ --doctest-modules omnimatch/ README.rst docs/example.rst

# The sympy_matching / sympy_wolfram Markdown documentation (README.md + docs/*.md)
# is executable: every example is a doctest, run by `tests/test_docs.py` in each
# package, so the docs are covered by the normal package test run below.
test-sympy:
	py.test rubi_rules/tests/ sympy_wolfram/ sympy_matching/

doctest:
	py.test --doctest-modules -k "not tests" omnimatch/ README.rst docs/example.rst
	py.test sympy_matching/tests/test_docs.py sympy_wolfram/tests/test_docs.py

check:
	flake8

lint:
	pylint omnimatch

coverage:
	py.test --cov=omnimatch --cov-report html --cov-report term tests/

api-docs:
	rmdir docs/api
	sphinx-apidoc -n -e -T -o docs/api omnimatch
	make docs

doc:
	python setup.py build_sphinx -W
