FROM python:3.11-bullseye

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH $PATH:/root/.local/bin
RUN apt-get update && apt-get upgrade -y && apt-get update
RUN apt-get install -y libgl1-mesa-dev

RUN mkdir /webcamrecorder
COPY pyproject.toml poetry.lock /webcamrecorder/
WORKDIR /webcamrecorder
RUN poetry install

CMD /bin/bash
