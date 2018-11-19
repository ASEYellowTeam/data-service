# data-service
_Manage the database_

[![Build Status](https://travis-ci.org/ytbeepbeep/data-service.svg?branch=master)](https://travis-ci.org/ytbeepbeep/data-service)
[![Coverage Status](https://coveralls.io/repos/github/ytbeepbeep/data-service/badge.svg?branch=master)](https://coveralls.io/github/ytbeepbeep/data-service?branch=master)

## Install
- `pip install -r requirements.txt`
- `python setup.py develop`


## Run the microservice
`python dataservice/app.py`

**Important note:** use python 3.6.


## Docker
[![Image size](https://images.microbadger.com/badges/image/ytbeepbeep/data-service.svg)](https://microbadger.com/images/ytbeepbeep/data-service)
[![Latest version](https://images.microbadger.com/badges/version/ytbeepbeep/data-service.svg)](https://microbadger.com/images/ytbeepbeep/data-service)

A Docker Image is available on the public Docker Hub registry. You can run it with the command below.

`docker run -d --name data-service ytbeepbeep/data-service`

**Important note:** if you need to expose the service outside you Docker installation (e.g. to third part services) use the option `-p 5002:5002`

#### Locally
You can also build your own image from this repository.
- Build with `docker build -t ytbeepbeep/data-service .`
- Run as usually, with the commands specified above
