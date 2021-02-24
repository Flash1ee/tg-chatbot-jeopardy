sudo docker run -d --rm -P -p 127.0.0.1:5432:5432 \
    -e POSTGRES_PASSWORD="1234" \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v /tmp/pgdata:/var/lib/postgresql/data \
    --name pg postgres:alpine