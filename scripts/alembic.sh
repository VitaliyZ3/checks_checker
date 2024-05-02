#!/bin/sh
cd ..
cd ./src
alembic revision --autogenerate -m "First commit"
alembic upgrade head