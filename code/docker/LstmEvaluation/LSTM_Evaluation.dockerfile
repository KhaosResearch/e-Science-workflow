FROM python:3.9.7-bullseye

LABEL Khaos Research Group <khaos.uma.es>

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install \
    numpy \
    pandas \
    sklearn \
    keras \
    typing \
    pathlib \
    tensorflow \
    typer


WORKDIR /usr/local/src/
COPY . /usr/local/src/

ENTRYPOINT ["python", "lstm_evaluation.py"]
