# sneaker-market

## 🚀 Установка и запуск

### 1. Клонирование репозитория

Для начала склонируйте репозиторий на локальную машину:

```bash
git clone https://github.com/Doozq/sneaker-market.git
cd sneaker-market
```

### 2. Установка зависимостей

Активируйте виртуальное окружение

```bash
python -m venv venv
# Для Windows
venv\Scripts\activate
# Для macOS/Linux
source venv/bin/activate
```

Установите зависимости
```bash
pip install -r requirements.txt
```

### 3. Запуск

Запустите сервер командой
```bash
cd market
python manage.py runserver
```

После чего перейдите по адрессу http://127.0.0.1:8000/

### 4. Админ

Для доступа к админ-панели перейдите по адрессу http://127.0.0.1:8000/admin
И войдите в существущий аккаунт (логин: admin, пароль: admin) либо создайте новый