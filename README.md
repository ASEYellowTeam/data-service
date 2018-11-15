# data-service microservice
_Manage the database_

[![Build Status](https://travis-ci.org/ASEYellowTeam/data-service.svg?branch=master)](https://travis-ci.org/ASEYellowTeam/data-service)
[![Coverage Status](https://coveralls.io/repos/github/ASEYellowTeam/data-service/badge.svg?branch=master)](https://coveralls.io/github/ASEYellowTeam/data-service?branch=master)


## Install
- `pip install -r requirements.txt`
- `python setup.py develop`


## Run the app
`python beepbeep/dataservice/run.py`

**Important note:** use python 3.6.


## Using Docker
- Build with `[sudo] docker build -t yellowteam/data-service .`
- Run with `[sudo] docker run -d --name data-service -p 5002:5002 yellowteam/data-service`
