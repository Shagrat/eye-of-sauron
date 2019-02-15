[![Build Status](https://travis-ci.org/Shagrat/sleepless.svg?branch=master)](https://travis-ci.org/Shagrat/sleepless)

# sleepless
Site monitoring tool for test assignment

# Install and set-up
- Clone repo
- Go to cloned repo root and: ```mkdir data && cd data && touch sites.yml```
- Use ```docker-compose up```
- Navigate browser to http://localhost:8000 (dashboard) http://localhost:8000/api/ (API documentation)

# sites.yml example
```
- https://www.google.ca/
- https://www.amazon.com
```

# API Docs
https://shagrat.github.io/sleepless/


# SocketIO
SocketIO and Celery (with RabbitMQ backend) added for background polling, emitting  will occur every 30 seconds

# Flower
http://localhost:5555

 