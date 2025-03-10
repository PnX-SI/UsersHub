
# Makefile for UsersHub

init_config:
	cp config/config.py.sample config/config.py
	cp config/settings.ini.sample config/settings.ini

run:
	. venv/bin/activate && flask run

start: run

install:
	./install_app.sh
	./install_db.sh

autoupgrade:
	. venv/bin/activate && flask db upgrade usershub@head
	. venv/bin/activate && flask db upgrade utilisateurs@head