#!/bin/sh

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
create extension citext;
select * FROM pg_extension;
EOF