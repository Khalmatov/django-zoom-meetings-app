# Django-Zoom-Meetings-App
<p>Приложение для Django, которое позволяет одной командой синхронизировать данные всех ваших конференций Zoom, включая участников конференций

> Предполагается, что файл `_config.py` по пути `myapp/management/commands` имеет следующее содержание:
```python
# myapp/management/commands/_config.py

MY_ID = 'myid' # id вашего аккаунта Zoom
JWT_TOKEN = 'jwt.token' # если нету, создайте JWT-App по адресу https://marketplace.zoom.us/user/build
```

## Оглавление
0. [Настройка рабочей среды](#Настройка-рабочей-среды)
1. [Команды](#Команды)
    1. [Синхронизизация конференций](#Синхронизизация-конференций)
    2. [Синхронизация участников конференций](#Синхронизация-участников-конференций)

## Настройка рабочей среды
Создайте проект Django и зарегистрируйте ваше приложение в нем:
```bash
python3 -m venv venv
source ./venv/bin/activate
django-admin startproject myproject
```
```python
# myproject/settings.py

INSTALLED_APPS = [
	...
	'bot-django',
	]
```

Не забудьте сделать миграции:
```bash
python manage.py makemigrations myapp
python manage.py migrate myapp
```

## Команды

Чтобы вывести список команд введите в консоли `python manage.py --help`. В ответ вы должны получить:
```bash
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[myapp]
    synchmeetings
    synchparticipants
```

### 1. Синхронизизация конференций
Команда `python manage.py synchmeetings` принимает два аргументы:
  1. **начало даты**  - строка в формате 2021-01-01
  2. **конец даты** - строка в формате 2021-01-01

Например:
```bash 
python manage.py synchmeetings 2021-03-27 2021-04-12
```
Команда "получает" по API все zoom-конференции созданные вами за период не больше месяца и не раньше полугода назад и
записывает полученные данные (конференции и участники) в вашу Базу Данных  
Если передать пустой аргумент команде, будут получены данные конференций за текущий день

### 2. Синхронизация участников конференций
Если по каким-либо причинам в БД отсутствуют участники конференций, наберите команду `python manage.py synchparticipants <uuid>`

Команда принимает один аргумент - `UUID конференции`

Например:
```bash 
python manage.py synchparticipants 41Uek17/RTS+uDgotvJOuA==
```
