FROM python:3.6
ADD ./ ./
RUN pip install -r requirements.txt
RUN python setup.py develop
EXPOSE 5002
CMD python beepbeep/dataservice/run.py
