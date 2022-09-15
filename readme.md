# API version roadmap
```python
#0.0.1 - API responding
#0.0.2 - Geting city data from URL
#0.0.3 - Geting data from DB
#0.0.4 - Uploading data to DB
# PoC 1
#0.1.0 - GET cities
#0.1.1 - GET routes-wroclaw
#0.1.2 - Running docker container [SKIPPED ISSUE #3]
#0.1.3 - PoC 1 code review
# PoC 2
#0.2.0 - GET top 5 closest stops
#0.2.1 - GET next departure for route from point A to B [HERE]
#0.2.2 - Unit tests for endpoints created in 0.2.x
#0.2.3 - ?
#0.3.0 - ?
#0.1.0 - ?
```

# How to use

## Config file
<b>Create config file according to template</b></br>
Name file ```secrets.py```

```python
#API
API_VERSION = "0.1.2"
API_URL = "XXX.XXX.XXX.XXX" #Your IP
API_PORT = 000 #HTTP/S port for running app

#DATABASE CONFIG
DB_USER = '' #DB user name
DB_USER_PASS = '' #DB user's password
DB_ADDR = '' #DB password with port

DB_URL = f'postgres://{DB_USER}:{DB_USER_PASS}@{DB_ADDR}/<table_name>' #DB table
```

## App running in Docker container

```bash
#1. clone git repository
git clone https://github.com/mateuszjasnowski/python_upskilling_poc_1.git

#2. copy config file to ./app_data/
cp <orginal path>/secrets.py <repo path>/app_data/

#3. build docker image
docker image build -t poc_app .

#4. run docker container from created image
docker run -p 443:443 -d poc_app
```

## App with debug mode on private machine

Developing version of app <br>

```bash
#1. clone git repository
git clone https://github.com/mateuszjasnowski/python_upskilling_poc_1.git

#2. create python virtual enviroment
python -m venv <venv_name>

#3. enter to python virtual enviroment
source ./<venv_dir>/bin/activate

#4. upgrade pip and install packages
python -m pip install -upgrade pip
pip install -r requirements

#5. start app on local machine
python main.py
```

## Used technologies
- Python
- Flask
- Docker
- PosgresDB
- Postman
