# Basic Operation Backend

This repository contains a small Flask calculator backend with a frontend and a MongoDB-backed `history` API.

## Features
- `/` serves the frontend
- `POST /calculate` accepts JSON `{ input1, input2, operator }` and returns `{ result }`
- `GET /history` returns past calculations stored in MongoDB

## Run locally with Docker
Commands assume Docker is installed and running.

1. Create a Docker network:

```bash
docker network create some-network
```

2. Start MongoDB on the network:

```bash
docker run -d --name some-mongo --network some-network mongo:latest
```

3. Build the app image (includes `pymongo`):

```bash
docker build -t basic-operation-backend:latest .
```

4. Run the app attached to the same network (exposes host port 80):

```bash
docker run -d \
  --name basic-operation-backend \
  --network some-network \
  -p 80:5000 \
  basic-operation-backend:latest
```

5. (Optional) Add a host alias for a nicer URL:

- macOS / Linux: edit `/etc/hosts` and add `127.0.0.1 basic-operation`
- Windows: edit `C:\Windows\System32\drivers\etc\hosts` and add `127.0.0.1 basic-operation`

Then access the app at `http://basic-operation` (or `http://localhost` or `http://localhost:80`).

## Test the API

- Calculate:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"input1":3,"input2":4,"operator":"+"}' http://localhost/calculate
```

- View history (latest):

```bash
curl http://localhost/history | jq .
```

## Environment variables
- `MONGO_URI` — MongoDB connection string (default `mongodb://some-mongo:27017`)
- `MONGO_DB` — database name (default `calculator_db`)
- `MONGO_COLLECTION` — collection name (default `calculations`)

Additional Mongo environment options:

- `MONGO_HOST` — Mongo host (default `some-mongo`)
- `MONGO_PORT` — Mongo port (default `27017`)
- `MONGO_USER` — Mongo username (optional)
- `MONGO_PASSWORD` — Mongo password (optional)

If `MONGO_URI` is provided it takes precedence. Otherwise `MONGO_USER` and `MONGO_PASSWORD` (if set) are used to build the connection URI.

### History pagination

You can paginate `/history` with query parameters `limit` and `skip`:

```bash
curl "http://localhost/history?limit=10&skip=0" | jq .
```

## Troubleshooting
- Check container logs:

```bash
docker logs basic-operation-backend --tail 200
docker logs some-mongo --tail 200
```

- Ensure both containers are on the same Docker network:

```bash
docker network inspect some-network
```

## Notes
- The app uses Gunicorn for serving in the container.
- The `/history` output timestamps are ISO-formatted UTC strings.
