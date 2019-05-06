
export FLASK_APP=server.py
export FLASK_ENV=development
export FLASK_DEBUG=1

ROOT_DIR=$(readlink -e "${0%/*}")

export PYTHONPATH=$PYTHONPATH:$ROOT_DIR


source $ROOT_DIR/venv/bin/activate
flask run --host=0.0.0.0 --port=5001
