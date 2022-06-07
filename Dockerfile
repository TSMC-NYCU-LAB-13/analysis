FROM python:3.10-slim
COPY . /analysis
WORKDIR /analysis
RUN apt-get update && \
    apt-get -yy install gcc libmariadb3 libmariadb-dev
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt

