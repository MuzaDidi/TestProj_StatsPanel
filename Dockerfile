FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE $APP_PORT

CMD alembic upgrade head && python app/main.py