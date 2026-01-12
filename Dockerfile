FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python manage.py collectstatic --noinput

EXPOSE 9000

CMD ["gunicorn", "OnlineShop.wsgi:application", "--bind", "0.0.0.0:9000", "--timeout", "120"] 