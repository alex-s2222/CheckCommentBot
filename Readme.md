# ТГ бот для ответа на комментариями под постами

## развертывание 

Скачать репозиторий

```bash
git clone https://github.com/alex-s2222/CheckCommentBot.git 
cd CheckCommentBot
```

Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Добавить ключи в example.env и переименовать
Нужно создать приложение https://my.telegram.org/auth
FILE_NAME=имя файла которое будет создаваться

```bash
vim excample.env 
mv excample.env .env
```

Запуск бота
При первом запуске нужно ввести номер телефона и ключ

```bash
python bot/main.py
```

## 🟥 Высокий приоритет

- [x] ответы на коментарии
- [x] проверку что как реагирует на пустое ''
- [x] проверку на создание файла
- [x] добавить ответ для комментариев
- [x] добавить ответ от аккаунта а не от бота

## ADMIN

- [x] Создать
- [x] Удалить
- [x] Просмотр