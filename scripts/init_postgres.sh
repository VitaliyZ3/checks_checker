sudo docker run --name postgres_db -p 5432:5432 -e POSTGRES_PASSWORD=root -e POSTGRES_DB=invoice_db -e POSTGRES_USER=backend_app -d postgres

sudo docker exec -it postgres_db psql -U "backend_app" -d "invoice_db"