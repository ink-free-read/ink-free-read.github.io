.PHONY: serve serve-node install

PORT = 8006

run:
	python3 -m http.server $(PORT)

pull-brand-assets:
	python3 pull_brand_assets.py
