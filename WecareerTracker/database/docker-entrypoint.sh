#!/bin/sh
exec psql init.sql
exec psql -h postgres -p 5432
