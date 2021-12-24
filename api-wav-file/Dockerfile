FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./api-wav-file /app

ENV PORT = 30000

EXPOSE 30000

CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "30000"]