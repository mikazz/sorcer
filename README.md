# sorcer

## Using
Redis - message broker

## Installing Redis

```sh
# Redis help
https://redis.io/topics/quickstart

# Redis.exe for Windows Download (skip if Linux)
https://github.com/microsoftarchive/redis/releases

# Installation (Skip if Windows)
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

# Run redis (Window Terminal 1)
redis-server

# Check if Redis is working (Window Terminal 2)
redis-cli ping

# Enable monitoring
redis.cli monitor (Window Terminal 3)
```

## Quick Start

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to http://localhost:5004 to view the app or to http://localhost:9181 to view the RQ dashboard.

## Architektura

* Walidacja i zabezpieczenie user input
* Dane o taskach nie moga znikac po restarcie serwera
* Preferowana formą wykonania asynchronicznego - osobny worker mogący działać potencjalnie na innej maszynie i jakiś system komunikacji między nimi (np. poprzez RabbitMQ albo Redisa).
* Zaprojektowaniu i zaimplementowanie REST API dla tego systemu.
* Mikroserwis powinien być napisany w języku Python.
* Rozwiązanie powinno zawierać testy automatyczne.
* Testy powinny być napisane w jakimś frameworku testowym np. wbudowany unittest lub pytest i powinny być uruchamialne niezależnie.
* Uruchomienie mikroserwisu powinno być maksymalnie zautomatyzowane (preferowane użycie Dockera lub podobnych narzędzi).
* Zlecenie pobrania tekstu z danej strony internetowej i zapis jej w systemie.
* Zlecenie pobrania wszystkich obrazków z danej strony i zapis ich w systemie.
* Obrazki wcale nie muszą mieć taga src.
* Sprawdzenie statusu zleconego zadania.
* Możliwość pobrania stworzonych zasobów (tekstu i obrazków)