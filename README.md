# HWSchool test

## Тестовое задание для hwschool

- **/tgbot** - первое задание
- **/codetest** - второе задание

### Первое задание

<img src="/images/image.png" width="800">
<img src="/images/image-1.png" width="800">
<img src="/images/image-2.png" width="800">
<img src="/images/image-3.png" width="800">


### Второе задание:

Переписал приложение на Flask с использованием SQLAlchemy. 
- Исправил некорректное отображение героев с ростом выше 180см и силой более 80
- Скорректировал запрос на отображение средних значений по полу
- Упаковал приложение для простоты запуска через run.py
- Скорректировал первоначальный запуск приложения и заполнения базы данных в случае обрыва соединения

#### Структура приложения:

```bash
superheroapp/
│
├── app/
│   ├── __init__.py          # Инициализация Flask приложения
│   ├── models.py            # Описание моделей SQLAlchemy
│   ├── routes.py            # Маршруты приложения
│   └── database.py          # Настройка базы данных
└── run.py                   # Запуск приложения Flask
```

#### Пример работы приложения:

<img src="/images/image-8.png" width="800">
<img src="/images/image-9.png" width="800">
<img src="/images/image-10.png" width="800">
<img src="/images/image-11.png" width="800">

#### Старая функциональность:

- **/codetest/initbd.py** - инициализация и создание БД
- **/codetest/bdcomplete.py** - заполнение БД с помощью superheroAPI
- **/codetest/create_csv_files.py** - вывод данных из БД в CSV формате
- **tall_strong_heroes.csv** - герои с ростом более 180 и силой больше 80
- **avg_by_gender.csv** - средние значения по полу
- **top_strength.csv** - ТОП-5 супергероев по силе

В ветке [v2](https://github.com/2rage/HWS_test_assignment/tree/v2) реализовал небольшое Flask-приложение, которое выводит данные таблиц через веб-интерфейс. Для оформления использовал Bootstrap.

Запуск приложения - `python3 create_csv_files.py`

#### Пример работы приложения:

<img src="/images/image-4.png" width="800">
<img src="/images/image-5.png" width="800">
<img src="/images/image-6.png" width="800">
<img src="/images/image-7.png" width="800">