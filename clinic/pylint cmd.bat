@echo off
copy nul pylint_log.txt
for /R %%f in (*.py) do (
	python -m pylint --rcfile=.pylintrc %%f >> pylint_log.txt
	echo ///////////////////////////////////////////////////////////////// >> pylint_log.txt
)