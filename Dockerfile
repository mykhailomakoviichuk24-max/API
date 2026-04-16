FROM python:3.12-slim

WORKDIR /app

# Копіюємо requirements і встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код
COPY . .

# Команду ми вже вказали в docker-compose, тому тут вона може бути як запасна
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]