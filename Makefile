check:
	find publications -name \*.json -exec echo -n ' -i ' \; -print0 | xargs jsonschema btcresearch-schema.json

site:
	rm -rf output
	rm -rf templates/publications
	mkdir output
	cp -R publications templates/
	python gensite.py
	cd output; \
	git init;\
	rm -rf publications;\
	git config user.name "Travis CI";\
	git config user.email "decker.christian+travis@gmail.com";\
	git add .;\
	git commit --quiet -m "Deploy to GitHub Pages";\
	git push --force "git@github.com:cdecker/btcresearch.git" master:gh-pages
