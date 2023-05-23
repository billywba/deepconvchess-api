FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root

COPY ./move_statistics.sql /docker-entrypoint-initdb.d/
