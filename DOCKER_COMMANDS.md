# Docker & Database Command Guide

A comprehensive quick-reference guide for managing your PostgreSQL database container using Docker and Docker Compose.

---

## 1. Docker Compose Basics

Your database container is defined in the [docker-compose.yml](file:///Users/aakashkoirala/assignment/docker-compose.yml) file and loads environment variables from the [.env](file:///Users/aakashkoirala/assignment/.env) file.

### 🚀 Starting the Database Container
To start the database in the background (detached mode):

```bash
docker-compose up -d
```

> [!NOTE]
> On the first startup, Docker will automatically download the `postgres:16` image and execute the database seeding script [seed.sql](file:///Users/aakashkoirala/assignment/seed.sql).

---

### 🛑 Stopping the Database Container
To stop the running database container without deleting your database data:

```bash
docker-compose down
```

---

### 🔄 Resetting and Re-seeding the Database
If you want to clear all tables, delete the persistent database volume, and **re-run the `seed.sql` initialization script**:

```bash
# Stops container and deletes the database volume
docker-compose down -v

# Starts database fresh with new seed data
docker-compose up -d
```

---

## 2. Monitoring & Debugging

Useful commands to check if your database is up, healthy, and configured correctly.

### 📋 Checking Container Status
To list running containers and check if the database port `5432` is bound correctly:

```bash
docker-compose ps
```

### 📝 Viewing Database Logs
To view the output and logs of the database (useful for checking if `seed.sql` loaded successfully):

```bash
# View all historical logs
docker-compose logs

# Follow/stream logs in real-time
docker-compose logs -f
```

---

## 3. Accessing PostgreSQL Directly

You can interact with the Postgres database instance inside the container using `psql` (the command-line interface).

### 🖥️ Open PostgreSQL Interactive Shell (`psql`)
Run this command to open the shell as the `admin` user inside the `mydatabase` database:

```bash
docker exec -it postgres-db psql -U admin -d mydatabase
```

Once inside `psql`, you can use the following database commands:

* **List all tables:** `\dt`
* **Describe a specific table structure:** `\d table_name`
* **Execute SQL query:** `SELECT * FROM customers LIMIT 5;`
* **Exit the psql shell:** `\q` or press `Ctrl + D`

---

## 4. Docker Cheat Sheet

| Action | Command | Description |
| :--- | :--- | :--- |
| **Start Database** | `docker-compose up -d` | Starts the postgres container in the background. |
| **Stop Database** | `docker-compose down` | Stops the postgres container. |
| **Full Database Reset** | `docker-compose down -v && docker-compose up -d` | Deletes volumes and recreates database fresh with `seed.sql`. |
| **Container Status** | `docker-compose ps` | Shows if the container is running or stopped. |
| **Tail Logs** | `docker-compose logs -f` | Streams real-time database server logs. |
| **Interactive CLI** | `docker exec -it postgres-db psql -U admin -d mydatabase` | Connects directly to the PostgreSQL database prompt. |
