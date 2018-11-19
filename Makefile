test:
	pytest -vv

setup:
	virtualenv -p python3 env && \
	pip3 install -r requirements.txt

run:
	python3 -m src.run
