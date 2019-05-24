FROM postgres:latest
# USER postgres
COPY init.sql /docker-entrypoint-initdb.d/init.sql
COPY . /database
# RUN chmod +x docker-entrypoint.sh
# ENV POSTGRES_HOST wecareer
EXPOSE 5432
# ENV POSTGRES_USER postgres
# ENV POSTGRES_PASSWORD postgres
# ENV POSTGRES_DB postgres1234
# ENTRYPOINT [ "./docker-entrypoint.sh" ]
