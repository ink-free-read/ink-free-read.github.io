.PHONY: serve serve-node install

PORT = 8006

run:
	python3 -m http.server $(PORT)

pull-icons:
	python3 pull_icons.py
