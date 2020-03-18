# sorcer

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


## Requirements
Python 3.7+
Redis - Message broker
RQ (Redis Queue) - Queueing jobs and processing them in the background with workers
Selenium and Webdriver - Sometimes no src is given..since it is getting rendered at runtime, so something like selenium would be useful

## Quick Start


## Usage
1. Run app.py
2. Run Redis server (i.e _Redis-x64-3.2.100/redis-server.exe)
3. Run worker.py
4. Open your browser to http://localhost:5000 to view the app or to http://localhost:5000/rq to view the RQ dashboard.


### Add new job

```bash
curl -X POST -F "page_url=https://www.wp.pl/" -F "function=get_text" http://127.0.0.1:5000/job
```

```json
{                                                                                                        
  "data": {                                                                                              
    "job_args": [],                                                                                      
    "job_download_url": "http://127.0.0.1:5000/jobs/368989ef-b4bb-40b1-a95f-7c41f327d7b5/download",      
    "job_enqueued_at": "Wed, 18 Mar 2020 16:30:15 GMT",
    "job_func_name": "jobs.get_text_job",                                                                
    "job_id": "368989ef-b4bb-40b1-a95f-7c41f327d7b5",                                                    
    "job_is_queued": true,                                                                               
    "job_kwargs": {                                                                                      
      "page_url": "https://www.wp.pl/"                                                                   
    },                                                                                                   
    "job_status_url": "http://127.0.0.1:5000/jobs/368989ef-b4bb-40b1-a95f-7c41f327d7b5"                  
  },                                                                                                     
  "status": "success"                                                                                    
}
```

### Check job status

```bash
curl -X GET http://127.0.0.1:5000/jobs/368989ef-b4bb-40b1-a95f-7c41f327d7b5
```

In progress

```json
{                                                                                                     
  "data": {                                                                                           
    "job_args": [],                                                                                   
    "job_dependent_ids": [],
    "job_download_url": "http://127.0.0.1:5000/jobs/368989ef-b4bb-40b1-a95f-7c41f327d7b5/download",   
    "job_ended_at": null,                                                                             ### Download scrapped page                                                                                                      
    "job_enqueued_at": "Wed, 18 Mar 2020 16:30:15 GMT",                                               
    "job_exc_info": null,                                                                             
    "job_func_name": "jobs.get_text_job",                                                             
    "job_id": "368989ef-b4bb-40b1-a95f-7c41f327d7b5",                                                 
    "job_is_queued": true,                                                                            
    "job_is_started": false,                                                                          
    "job_kwargs": {                                                                                   
      "page_url": "https://www.wp.pl/"                                                                
    },                                                                                                
    "job_meta": {},                                                                                   
    "job_result": null,                                                                               
    "job_started_at": null,                                                                           
    "job_status": "queued",                                                                           
    "job_status_url": "http://127.0.0.1:5000/jobs/368989ef-b4bb-40b1-a95f-7c41f327d7b5",              
    "job_timeout": 60                                                                                 
  }                                                                                                   
}
```

Done

```bash
curl -X GET http://127.0.0.1:5000/jobs/e2d1cf06-3300-4780-9b0b-e9e8eab52ccb
```

```json
{
  "data": {
    "job_args": [],
    "job_dependent_ids": [],
    "job_download_url": "http://127.0.0.1:5000/jobs/e2d1cf06-3300-4780-9b0b-e9e8eab52ccb/download",
    "job_ended_at": "Wed, 18 Mar 2020 17:00:56 GMT",
    "job_enqueued_at": "Wed, 18 Mar 2020 17:00:46 GMT",
    "job_exc_info": null,
    "job_func_name": "jobs.get_images_job",
    "job_id": "e2d1cf06-3300-4780-9b0b-e9e8eab52ccb",
    "job_is_queued": false,
    "job_is_started": false,
    "job_kwargs": {
      "page_url": "https://www.google.pl/"
    },
    "job_meta": {},
    "job_result": null,
    "job_started_at": null,
    "job_status": "finished",
    "job_status_url": "http://127.0.0.1:5000/jobs/e2d1cf06-3300-4780-9b0b-e9e8eab52ccb",
    "job_timeout": 60
  }
}
```

### Download Ready Job

```bash
curl -X GET http://127.0.0.1:5000/jobs/e2d1cf06-3300-4780-9b0b-e9e8eab52ccb/download --output download.zip
```

```json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 14180  100 14180    0     0  14180      0  0:00:01 --:--:--  0:00:01  177k
```