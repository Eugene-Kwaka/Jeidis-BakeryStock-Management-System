# Stock-Management-System
This is a stock management system for Jeidis Bakery where they can track all the items in stock and manage them accordingly.


# Table of Contents
- [Background](#background)
- [Minimum Requirements](#minimum-requirements)
- [Quickstart](#quickstart)
- [Database SetUp](#database-setup)
- [Database Migration](#database-migration)

## Background
This project is a Inventory Management System for a bakery where the stock items used are tracked and managed accordingly. The application has an authentication system and Filter functionality that can provide an output in the CSV format.
The project applies Django's MVT(Model View Templates) architecture. It has a CRUD (Create Read Update Delete) application for the stock items in which the logged in user can manipulate the items.
The project is written with Function-Based Views (FBV) with focus on core fundamentals which are easy to read, understand and implement.

## Minimum Requirements
This project supports Ubuntu Linux 20.04 and Windows OS with their previous stable releases. It has not been tested on Mac OS.

- [Python3](https://www.python.org/downloads/)
- [Django 3.2](https://www.djangoproject.com/)
- [Bootstrap 4.3.1](https://getbootstrap.com/docs/4.3/getting-started/introduction/)
- [PostgreSQL 14.2+](http://www.postgresql.org/)
- [Git](https://git-scm.com/downloads)


## Quickstart
```bash
$ mkdir stockinventory
$ cd stockinventory
$ git init
$ git clone https://github.com/Eugene-Kwaka/Stock-Management-System.git
$ cd Stock-Management-System
$ sudo apt install python3-pip python3-django
$ sudo apt install python3-venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Database Setup
``` settings.py
'ENGINE': 'django.db.backends.postgresql',
'NAME': ('DB_NAME'),
'USER': ('DB_USER'),
'PASSWORD': ('DB_PASSWORD'),
'HOST': ('DB_HOST'),
'PORT': ('DB_PORT')
```

## Database Migration
```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
