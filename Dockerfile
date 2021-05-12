# first stage
FROM python:3.8 AS builder

WORKDIR /opt/flare/src

COPY requirements.txt .

COPY ./src .

RUN adduser --disabled-login --uid 10001 flare
USER flare

ENV PATH=/flare/.local:$PATH
ENV PATH=/flare/.local/bin:$PATH
RUN pip install --user -r requirements.txt

ENTRYPOINT [ "/bin/sh", "-c" , "/opt/flare/src/run_flare.sh" ]