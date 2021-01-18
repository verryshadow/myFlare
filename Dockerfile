# first stage
FROM python:3.8 AS builder
COPY requirements.txt .

ENV PATH=/root/.local:/root/.local/bin:$PATH

# install dependencies to the local user directory (eg. /root/.local)
RUN pip3 install --user -r requirements.txt

# TODO multistage dockerfile, see https://www.docker.com/blog/containerized-python-development-part-1/
COPY --from=builder /root/.local/bin /root/.local
COPY ./src .

# update PATH environment variable
ENV FLASK_APP=run_flask.py
ENV PATH=/root/.local:/root/.local/bin:$PATH

CMD [ "python", "./run_flask.py" ]
