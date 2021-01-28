# first stage
FROM python:3.8 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
ENV PATH=/root/.local:$PATH
RUN pip install --user -r requirements.txt

# copy only the dependencies installation from the 1st stage image
COPY ./src .

CMD [ "python3", "run_server.py" ]
