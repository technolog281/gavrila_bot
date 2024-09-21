# установка базового образа (host OS)
FROM python:3.9

# установка рабочей директории в контейнере
WORKDIR /gavrila_code

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей
RUN pip install -r requirements.txt

# копирование содержимого локальной директории src в рабочую директорию
COPY gavrila_bot/ .

# команда, выполняемая при запуске контейнера
CMD [ "python", "./aiogram_run.py" ]