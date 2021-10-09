isort = ./env/bin/python3 -m isort app bot
black = ./env/bin/python3 -m black app bot
flake8 = ./env/bin/python3 -m flake8 app bot

start-bot:
	./env/bin/python3 -m bot.main

set-env:
	virtualenv -p python3 env

install:
	./env/bin/pip install -r requirements.txt

format:
	$(isort)
	$(black)

lint:
	$(flake8)
	$(isort) --check-only --df
	$(black) --check --diff
