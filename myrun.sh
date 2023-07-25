pip install -r requirements.txt

docker-compose up -d

cd src

python3 run_server.py $DEBUG
