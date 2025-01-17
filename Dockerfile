FROM python:3.8

RUN mkdir /app

COPY /shortener /app/shortener
COPY pyproject.toml /app
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000
CMD ["gunicorn", "shortener:app", "-b 0.0.0.0:8000"]
