<!-- ABOUT THE PROJECT -->
## BETLINE
Тестовое задание, платформа для ставок на определнные события.
Старался следовать слоистой архитектуре, проект представляет собой 2 микросервиса, запускающиекся отдельно каждый в свое докер контейнере.
Общение между сервисами осуществляется через кафку

## GETTING STARTED

1. Проект использует make команды, можно поставить себе make, а можно воспользоваться докер командами
[windows make](https://gnuwin32.sourceforge.net/packages/make.htm)
ну докер думаю у всех есть, как и гит

2. Стянуть проект к себе
```sh
git clone https://github.com/rianoneq/betline
```

4. открыть 2 терминала, с одного зайти в папку bet_maker, с другого в line_provider
```sh
cd betline/bet_maker
```
```sh
cd betline/line_provider
```

далее действия дублируются на каждый из терминалов (сервисов)

5. Создать .env в корне проекта рядом с .env.example и заполнить его такими же данными

6. Поднять сервис командой make либо docker
   - make
    ```sh
      make app
    ```
   - docker
  
     - line_provider
      ``` sh
         docker compose -f docker_compose/app.yaml -f docker_compose/storages.yaml -f docker_compose/messaging.yaml -p line-provider up -d --build
      ```
     - bet_maker
      ``` sh
         docker compose -f docker_compose/app.yaml -f docker_compose/storages.yaml -p bet-maker up -d --build
      ```

7. Провести миграции
   - make
   ``` sh
    make migrate
   ```
   - docker
  
     - line_provider
      ``` sh
         docker exec -it line-main-app alembic upgrade heads
      ```
     - bet_maker
      ``` sh
         docker exec -it bet-main-app alembic upgrade heads
      ```

8. Перезапустить bet_maker
   - make
      ``` sh
         make app
      ```
   - docker
      ``` sh
         docker compose -f docker_compose/app.yaml -f docker_compose/storages.yaml -p bet-maker up -d --build
      ```
9. Перейти в доки
  - http://localhost:8001/api/docs
  - http://localhost:8000/api/docs

10. Проверить логи
    - make
        ```sh
          make app-logs
        ```
    - docker
       - line_provider
        ```sh
      docker logs -f line-main-app
        ```
     - bet_maker
       ```sh
        docker logs -f bet-main-app
        ```
11. Запустить тесты
   - make
        ```sh
         make tests
        ```
   - docker
     - line_provider
      ```sh
      docker exec -it line-main-app pytest
     ```
     - bet_maker
      ```sh
      docker exec -it bet-main-app pytest
     ```

Помимо того что описано в тз реализовал обработку новых ставок в сервисе событий. То есть когда на определнное событие делается ставка (на победу первой команды по тз), кэф это ставки уменьшается на 10% от суммы ставки.
Добавил я это потому что посчитал странным, что сумма ставки и коэффициент события никак не взаимодействуют и непонятно зачем нужны.

Надеюсь что все запустилось и корректно работает. Буду рад обсудить выполнение тестового задания с вами!
