FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY . /app


ENV PORT=8000

# runserver только для dev
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:${PORT}"
