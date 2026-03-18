# Клуб «Горбатая гора» — База данных

## Требования
- PostgreSQL 14+
- DBeaver (или любой SQL клиент)

## Порядок запуска

### 1. Создание схемы
Открыть `createdb.sql` → **Alt+X**

### 2. Генерация тестовых данных
Установить зависимости:
```bash
pip install faker
```

Запустить генератор:
```bash
python generate_data.py
```

### 3. Начальное наполнение
Открыть `init_data.sql`  *Alt+X*


Скрипт создаст файл `test_data.sql`.
Открыть `test_data.sql` в DBeaver → *Alt+X*
