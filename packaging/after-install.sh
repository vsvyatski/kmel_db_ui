cd /opt/kmeldb-ui

chmod 755 ./kenwooddbgen.sh

# creating __pycache__ folders and adding proper permissions so that Python can generate
# compiled bytecode running under standard user account
mkdir ./__pycache__
chmod 777 ./__pycache__
mkdir ./kmeldb_cli/kmeldb/__pycache__
chmod 777 ./kmeldb_cli/kmeldb/__pycache__

sh ./install-venv.sh

cd -
