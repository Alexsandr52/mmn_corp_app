# Используем официальный образ Python как базовый
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для приложения Flask (по умолчанию Flask использует порт 5000)
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
