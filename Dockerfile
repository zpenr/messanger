FROM python:3.12.3

WORKDIR /app

ADD . /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "run:application"]