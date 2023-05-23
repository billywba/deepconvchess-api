FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root

COPY ./move_statistics.db /docker-entrypoint-initdb.d/
