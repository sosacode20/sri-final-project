FROM docker.uclv.cu/fedora:37

WORKDIR /irs-final-project

COPY src/ ./src
COPY cli.py .
COPY install.py .
COPY requirements.txt .
COPY Pre-entrega.md .
COPY README.md .
COPY Project-architecture.excalidraw.svg .
COPY .gitignore .
COPY .git ./.git
COPY data/ ./data
COPY irs_data/ ./irs_data

RUN dnf install python3-pip -y
RUN python3 -m venv ./.venv
RUN source ./.venv/bin/activate
RUN pip install -r ./requirements.txt
RUN python3 ./install.py

CMD [ "bash" ]
