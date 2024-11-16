FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gnupg2 lsb-release && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get remove -y --auto-remove curl gnupg2 lsb-release && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /setup_22.x

WORKDIR /javascript-coderun

COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run"]
