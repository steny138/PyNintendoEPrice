
```
# create a postgres container
docker run --name ns_web -it -e POSTGRES_PASSWORD=1qaz2wsx -e POSTGRES_USER=admin\
   -d -p 5432:5432 postgres

# run psql command with docker container - 1
docker run -it --link ns_web:postgres --rm postgres sh -c 'exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U admin'

# run psql command with docker container - 2
docker exec -it  ns_web sh -c " psql -U admin"

# -t 選項讓Docker分配一個虛擬終端（pseudo-tty）並綁定到容器的標準輸入上， 
# -i 則讓容器的標準輸入保持打開


```

`  -v /Volumes/Macintosh\ HD/Docker/data:/var/lib/postgresql/data/pgdata  `