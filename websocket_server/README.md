# WebSocket Server

## APIs

1. Dimmer debug console: `/dimmer/<dimmer_name>/`
2. Turn on the dimmer: `/dimmer/<dimmer_name>/turn_on/`
3. Turn off the dimmer: `/dimmer/<dimmer_name>/turn_off/`

## Web Sockets

`ws://<hostname>/ws/dimmer/<dimmer_name>/`

## Requirement

```
pip install channels
pip install channels_redis
```

You will probably install `redis`, which could be different based on your platform.

## Start

`python manage.py runserver /0.0.0.0:8765`
