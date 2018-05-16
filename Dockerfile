FROM python:3.6-alpine

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app
CMD ["python",  "main.py"]
