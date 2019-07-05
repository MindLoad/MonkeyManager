# Initial prepares

LINT_TARGETS := $(shell echo .)
LINT_ARGS := $(shell echo -r)

run:
	python monkey.py
lint_pylint:
	@echo '[PYLINT]'
	pylint --rcfile=.pylintrc / tools/
lint_pycodestyle:
	@echo '[PYCODESTYLE]'
	pycodestyle $(LINT_TARGETS) --config=.pycodestyle
lint_safety:
	safety check -r Pipfile
inspect:
	@echo '[BANDIT]'
	@$(CMD_PREFIX) bandit $(LINT_ARGS) $(LINT_TARGETS)
check: lint_pycodestyle inspect lint_pylint lint_safety
