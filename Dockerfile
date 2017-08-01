FROM python:2.7-alpine

RUN pip install click requests
ADD load.py /load.py

ENTRYPOINT ["python", "/load.py"]
