FROM python:3.10.6-buster
COPY divvy /divvy
COPY requirements_prod.txt /requirements_prod.txt
RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt
CMD uvicorn divvy.interface_api.api:app --host 0.0.0.0 --port $PORT
