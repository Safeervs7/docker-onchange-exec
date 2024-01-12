FROM python:3.11.6-alpine3.18
WORKDIR /on-change
ENV PYTHONUNBUFFERED=1

RUN pip install docker
COPY on-change.py /usr/bin/on-change.py

CMD ["on-change.py"]
