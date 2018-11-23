FROM python:3.6
MAINTAINER Yellow Team ytbeepbeep@gmail.com
ADD ./ ./
RUN pip install -r requirements.txt
RUN python setup.py develop
EXPOSE 5002
CMD python dataservice/app.py
