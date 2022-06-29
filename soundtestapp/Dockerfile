FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . ./app

ENV PORT = 8000

EXPOSE 8000

CMD ["python", "soundtestapp/manage.py", "runserver", "0.0.0.0:8000"]