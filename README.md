# Сервис сжатия потока сообщений о событиях zenoss

- **compresszenoss.py** - основной модуль для сжатия сообщений zenoss из топиков kafka
- **conf.py** - конфиг
- **screen-compresszenoss-chi.service** - сервис systemd
- **screen-compresszenoss-irk.service** - сервис systemd
- **screen-compresszenoss-krsk.service** - сервис systemd
- **screen-ws.service** - сервис systemd для публикации сообщений через websocket
- **ws_client.py** - тестовый websocket клиент
- **ws_server.py** - websocket сервер
- **ws_server.sh** - скрипт запуска websocket сервера
- **zenoss-chi.sh** - скрипт запуска службы
- **zenoss-irk.sh** - скрипт запуска службы
- **zenoss-krsk.sh** - скрипт запуска службы
