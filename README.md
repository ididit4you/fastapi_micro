# Base template for microservices


# Alembic migrations
Make migration
```
alembic revision -m "Migration name" --autogenerate --head head
```

Migrate: 
```
alembic revision -m "Prices are unique by date and ticker" --autogenerate --head head
```