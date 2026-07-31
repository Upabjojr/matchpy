init:
	pip install .[develop]

test:
	py.test tests/ --doctest-modules matchpy/ README.rst docs/example.rst

# The sympy_matching / sympy_wolfram READMEs document Mathematica's pattern semantics
# and every example in them is a doctest; `tests/test_readme.py` in each package runs
# them, so they are covered by the normal package test run below.
test-sympy:
	py.test rubi_rules/tests/ sympy_wolfram/ sympy_matching/

doctest:
	py.test --doctest-modules -k "not tests" matchpy/ README.rst docs/example.rst
	py.test sympy_matching/tests/test_readme.py sympy_wolfram/tests/test_readme.py

check:
	flake8

lint:
	pylint matchpy

coverage:
	py.test --cov=matchpy --cov-report html --cov-report term tests/

api-docs:
	rmdir docs/api
	sphinx-apidoc -n -e -T -o docs/api matchpy
	make docs

doc:
	python setup.py build_sphinx -W
