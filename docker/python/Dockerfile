FROM python:3.9
WORKDIR /var/app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY /src .
CMD [ "python", "/var/app/main.py" ]
