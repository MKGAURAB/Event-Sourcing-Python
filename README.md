# Event Sourcing 

This project is just to sharpen my skill with Python development. EventSourcing is my fav architectural approach. Hence you see it here.
It's just the event sourcing part done in a cold winter evening. Someday will try to add the projection part.

## Requirements

You have to have Python 3.7+ installed on your local system nad docker + docker-compose.

## Setup

1. Clone this repository

2. Install the Python dependencies

In a command line - run

`pip3 install -r requirements.txt`

If you are using a virtual environment (venv) replace the pip3 with simply pip.

3. Enable docker container

`docker-compose up -d`

It will download and run the event store. Try to access it via localhost:2113

```
username: admin
password: changeit
```

4. Start FastAPI process
`python3 main.py`
Open local API docs http://localhost:5000/docs

Generated events that can
be seen by accessing: http://localhost:2113/web/index.html#/streams
