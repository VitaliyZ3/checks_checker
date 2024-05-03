#!/bin/sh
cd ..
cd ./src
alembic revision --autogenerate -m "Addedf File Type"
alembic upgrade head