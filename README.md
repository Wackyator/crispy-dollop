# LibMS

## Setup
- Install uv.
- Run `uv sync`.

## Running 
- Activate the venv.
- Run `alembic upgrade head`.
- Run `python -m app`.
- That's it.
- Alternatively, it can be run via docker.
```bash
docker build -t lib-ms .
docker run -d --name lib-ms-app -p 8000:8000 lib-ms 
```

## Screenshots
- Screenshots are available in the screenshots folder.

## Deployed Application
- Deployed application can be found [here](https://gladly-choice-monkfish.ngrok-free.app/)
