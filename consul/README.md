# Usage


## 1. clone repository
```

```
docker build -t reverse-proxy .

## 2. run containers
```
$ docker-compose up -d --build
```

this docker-compose file runs 5 containers
* consul
* reverse-proxy (load balancer)
* web (flask application)
* redis
* registrator

in `docker-compose.yml`, we provide docker.sock file to registrator, using the command:

```
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock
```

this way, registrator can see docker logs, and register containers once they are launched, or de-register them once they are stopped.

type `docker ps` to view those containers.

## 3. visit consul

after step 2, check localhost:8500 to verify that registrator successfully registered services labeled `redis` and `web`.

## 4. scale webservices, visit consul again

now let's have 5 webservices instead of 1:


```
$ docker-compose scale web=5
```

After scaling, visit:

- traefik webui: localhost:8080
- consul webui: localhost:8500 (consul should have 5 services under "web")
- web service access using traefik: localhost:8081 (try to refresh page and see host IDs. traefik should do loadbalancing on web services)




