# data-service
_Manage the database_ • [data-service.yellowteam.ml](http://data-service.yellowteam.ml)

[![Build Status](https://travis-ci.org/ASEYellowTeam/data-service.svg?branch=master)](https://travis-ci.org/ASEYellowTeam/data-service)
[![Coverage Status](https://coveralls.io/repos/github/ASEYellowTeam/data-service/badge.svg?branch=master)](https://coveralls.io/github/ASEYellowTeam/data-service?branch=master)

## Install
- `pip install -r requirements.txt`
- `python setup.py develop`


## Run the app
`python beepbeep/dataservice/run.py`

**Important note:** use python 3.6.


## Using Docker
[![Image size](https://images.microbadger.com/badges/image/ytbeepbeep/data-service.svg)](https://microbadger.com/images/ytbeepbeep/data-service)
[![Latest version](https://images.microbadger.com/badges/version/ytbeepbeep/data-service.svg)](https://microbadger.com/images/ytbeepbeep/data-service)

A Docker Image is available on the public Docker Hub registry. You can run it with the command below.

`[sudo] docker run -d --name data-service -p 5002:5002 ytbeepbeep/data-service`

#### Locally
You can also build your own image from this repository.
- Build with `[sudo] docker build -t data-service .`
- Run with `[sudo] docker run -d --name data-service -p 5002:5002 data-service`
