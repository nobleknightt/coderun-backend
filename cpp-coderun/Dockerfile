FROM python:3.12-slim-bookworm

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends clang && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /cpp-coderun

COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run"]
