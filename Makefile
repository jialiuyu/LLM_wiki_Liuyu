.PHONY: check search

check:
	python3 scripts/wiki_check.py

search:
	@test -n "$(q)" || (echo 'Usage: make search q="your query"' && exit 2)
	python3 scripts/wiki_search.py "$(q)"

