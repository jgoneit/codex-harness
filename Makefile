.PHONY: test

test:
	@if python3 -c "import pytest" >/dev/null 2>&1; then \
		python3 -m pytest -q; \
	else \
		PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v; \
	fi
