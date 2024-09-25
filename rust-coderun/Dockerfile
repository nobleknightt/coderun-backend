FROM python:3.12-slim-bookworm

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal && \
    apt-get remove -y --auto-remove curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /rust-coderun

COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run"]
