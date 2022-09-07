## API version roadmap
```python
#0.0.1 - API responding
#0.0.2 - Geting city data from URL
#0.0.3 - Geting data from DB
#0.0.4 - Uploading data to DB
#0.1.0 - GET cities
#0.1.1 - GET routes-wroclaw [HERE]
#0.1.2 - PoC 1 code review
#0.2.0 - PoC 2 TODO
#0.2.1 - ?
```

## Used technologies
- Python
- Flask
- Docker
- PosgresDB
- Postman

# How to use (developing version)

Curently only at developing version

##APP INSTALATION
```bash
git clone <repo url>

#not required but sugested:
python -m venv <venv_name>

#in venv if used
pip install -r requirements
```
##Create app config file <i>app_data/secrets.py</i> (Refer to template file)
```python
#API
API_VERSION = "0.0.3" #API VERSION HERE
API_URL = "XXX.XXX.XXX.XXX" #API URL HERE

#DATABASE
DB_USER = '' #USERNAME for DB SERVER
DB_USER_PASS = '' #PASSWORD for DB SERVER
DB_ADDR = '' #DB SERVER's ADDRESS

DB_URL = f'postgres://{DB_USER}:{DB_USER_PASS}@{DB_ADDR}'
```

