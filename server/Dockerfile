FROM python:3.12-alpine
WORKDIR /srv
COPY . /srv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=app
CMD ["python","app.py"]