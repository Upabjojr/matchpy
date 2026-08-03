@ECHO off
if /I %1 == init goto :init
if /I %1 == test goto :test
if /I %1 == doctest goto :doctest
if /I %1 == check goto :check
if /I %1 == lint goto :lint
if /I %1 == coverage goto :coverage
if /I %1 == api-docs goto :apidocs
if /I %1 == docs goto :docs

goto :eof

:init
    pip install .[tests,develop]
goto :eof

:test
	py.test tests\ --doctest-modules omnimatch\ README.rst docs\example.rst
goto :eof

:doctest
	py.test --doctest-modules -k "not tests" omnimatch\ README.rst docs\example.rst
goto :eof

:check
    flake8
goto :eof

:lint
	pylint --reports=no omnimatch
goto :eof

:coverage
	py.test --cov=omnimatch --cov-report html --cov-report term tests\
goto :eof

:apidocs
	rmdir /s /q docs\api
	sphinx-apidoc -e -T -o docs\api omnimatch
goto :docs

:docs
	cd docs
	make html
	cd ..
goto :eof

