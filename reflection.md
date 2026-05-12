## Reflection

### Config (Factor III)

Using a `.env` file is better than writing passwords directly in the code because it keeps sensitive information secure and easier to manage. If database usernames and passwords are hardcoded into the application, anyone who can access the source code can see those credentials. This becomes risky when sharing code through GitHub or working in a team. By storing configuration values inside a `.env` file, the application can read them dynamically without exposing secrets in the codebase. It also makes the application more flexible because different environments such as development, testing, and production can use different database settings without changing the actual code. This improves security, maintainability, and portability.

### Backing Services (Factor IV)

Treating the database as a separate service is useful because the application and database remain independent from each other. PostgreSQL runs inside its own Docker container, which means it can be started, stopped, updated, or replaced without affecting the main application code. This separation makes the system modular and easier to manage. It also allows developers to connect different applications to the same database service when needed. Using Docker Compose further simplifies communication between services and ensures consistency across environments.

### Dev/Prod Parity (Factor X)

Docker helps make development and production environments similar because the same container configuration can run everywhere. Developers use the same PostgreSQL image, environment variables, and setup process locally that will also be used in production. This reduces issues like “it works on my machine” because everyone works with the same dependencies and configurations. Docker also ensures that the database setup, including the automatic execution of `seed.sql`, behaves consistently across systems. As a result, development, testing, and deployment become more reliable and predictable.
