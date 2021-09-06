export FLASK_ENV=development
export FLASK_DEBUG=1

ROOT_DIR=$(readlink -e "${0%/*}")
source $ROOT_DIR/venv/bin/activate

flask run --port=5001
