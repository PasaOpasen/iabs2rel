
test:
	python -m pytest tests

doctest:
	python -m pytest --doctest-modules \
		--ignore-glob='**/__*' \
			./iabs2rel
